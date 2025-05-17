# app.py

import streamlit as st
import pandas as pd
import pickle
import plotly.graph_objs as go
from datetime import timedelta
import os

st.set_page_config(page_title="Stock Price Forecasting", layout="wide")

st.title("📈 Stock Price Forecasting")
st.markdown("""
Select the company ticker and the number of days to forecast the closing price using a pre-trained ARIMA model.
""")

DATA_FILE = "Prices_Cleaned.csv"
MODEL_FILE = "arima_model.pkl"

# Check if data file exists
if not os.path.exists(DATA_FILE):
    st.error(f"Data file '{DATA_FILE}' not found. Please make sure it is in the app directory.")
    st.stop()

# Load data
df = pd.read_csv(DATA_FILE)

if "symbol" not in df.columns:
    st.error("Data file must contain a 'symbol' column with company tickers.")
    st.stop()

df["date"] = pd.to_datetime(df["date"], errors="coerce")
if df["date"].isnull().any():
    st.error("Invalid dates found in 'date' column. Please check the data file.")
    st.stop()

df = df.sort_values("date")

# Get list of unique tickers
tickers = sorted(df["symbol"].unique())

# UI inputs
col1, col2 = st.columns(2)

with col1:
    ticker = st.selectbox("Select Company (Ticker)", options=tickers)

with col2:
    days_options = [7, 14, 30, 60, 90, 180, 365]
    forecast_days = st.selectbox("Select Forecast Days", options=days_options, index=2)

if st.button("Generate Forecast"):
    # Check model file
    if not os.path.exists(MODEL_FILE):
        st.error(f"Model file '{MODEL_FILE}' not found. Please ensure the ARIMA model file is available.")
        st.stop()

    try:
        # Load ARIMA model
        with open(MODEL_FILE, "rb") as f:
            model_fit = pickle.load(f)

        # Filter data for selected ticker
        company_data = df[df["symbol"] == ticker].copy()
        if company_data.empty:
            st.error(f"No data found for ticker '{ticker}'.")
            st.stop()

        company_data.set_index("date", inplace=True)
        company_data = company_data.sort_index()

        if "close" not in company_data.columns:
            st.error("Column 'close' not found in the data for the selected ticker.")
            st.stop()

        # Generate forecast
        forecast = model_fit.get_forecast(steps=forecast_days)
        forecast_df = forecast.summary_frame()

        start_date = company_data.index.max() + timedelta(days=1)
        forecast_index = pd.date_range(start=start_date, periods=forecast_days)
        forecast_df["date"] = forecast_index
        forecast_df.set_index("date", inplace=True)

        # Last 100 actual data points for plotting
        recent_actual = company_data["close"].iloc[-100:]

        # Plot using Plotly
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=recent_actual.index,
            y=recent_actual.values,
            mode="lines",
            name="Actual Closing Price (Last 100 Days)",
            line=dict(color="blue")
        ))
        fig.add_trace(go.Scatter(
            x=forecast_df.index,
            y=forecast_df["mean"],
            mode="lines",
            name="Forecast",
            line=dict(color="orange", dash="dash")
        ))
        fig.add_trace(go.Scatter(
            x=forecast_df.index.tolist() + forecast_df.index[::-1].tolist(),
            y=forecast_df["mean_ci_upper"].tolist() + forecast_df["mean_ci_lower"][::-1].tolist(),
            fill="toself",
            fillcolor="rgba(128,128,128,0.2)",
            line=dict(color="rgba(255,255,255,0)"),
            hoverinfo="skip",
            name="95% Confidence Interval"
        ))

        fig.update_layout(
            title=f"{ticker} Closing Price Forecast for Next {forecast_days} Days",
            xaxis_title="Date",
            yaxis_title="Price",
            template="plotly_white",
            height=500
        )

        st.plotly_chart(fig, use_container_width=True)

        # Display forecast table
        forecast_table = forecast_df[["mean", "mean_ci_lower", "mean_ci_upper"]].reset_index()
        forecast_table.columns = ["Date", "Forecasted Price", "Lower 95% CI", "Upper 95% CI"]
        forecast_table = forecast_table.round(2)

        st.subheader("Forecast Details")
        st.dataframe(forecast_table, use_container_width=True)

    except Exception as e:
        st.error(f"An error occurred while forecasting: {str(e)}")
