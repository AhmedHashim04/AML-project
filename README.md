# Stock Price Forecasting App

A **Streamlit web application** for forecasting stock closing prices using a pre-trained ARIMA model. Easily select a stock ticker and forecast horizon, visualize predictions with confidence intervals, and review detailed results—all in your browser.

---

## Features

- 📈 **Interactive Forecasting:** Choose a stock ticker and forecast period (7–365 days).
- 🧠 **Pre-trained ARIMA Model:** Fast, reliable time series forecasting.
- 📊 **Rich Visualization:** Plotly charts show actual vs. forecasted prices with 95% confidence intervals.
- 🗃️ **Forecast Table:** Tabular view of predictions and confidence bounds.
- 🏢 **Multi-Ticker Support:** Analyze multiple stocks from your dataset.

---

## Project Structure

- `main.py` — Streamlit app entry point.
- `Prices_Cleaned.csv` — Cleaned historical stock prices (`date`, `symbol`, `close` columns required).
- `arima_model.pkl` — Pre-trained ARIMA model (pickle format).
- `README.md` — Project documentation.

---

## Getting Started

### 1. Clone the Repository

```sh
git clone <your-repo-url>
cd <project-directory>
```

### 2. Install Dependencies

Create a virtual environment and install required packages:

```sh
python -m venv venv
# On Unix/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

pip install streamlit pandas plotly
```

> **Note:** If your ARIMA model uses other libraries (e.g., `statsmodels`), install them as well.

### 3. Prepare Data and Model

- Place your cleaned stock price data as `Prices_Cleaned.csv` in the app directory.
    - Required columns: `date`, `symbol`, `close`
- Place your pre-trained ARIMA model as `arima_model.pkl` in the app directory.

### 4. Run the App

```sh
streamlit run main.py
```

---

## Usage

1. **Select Company (Ticker):** Choose a stock ticker from the dropdown.
2. **Select Forecast Days:** Pick the forecast horizon (7, 14, 30, 60, 90, 180, or 365 days).
3. **Generate Forecast:** Click the button to view forecast charts and tables.

---

## Data & Model Requirements

- **CSV File:** `Prices_Cleaned.csv`
    - Columns: `date` (YYYY-MM-DD), `symbol` (ticker), `close` (closing price)
- **Model File:** `arima_model.pkl`
    - Must be a pickled ARIMA model trained on your data.

---

## Error Handling

- The app checks for missing files and required columns.
- Invalid or missing data triggers clear error messages.

---

## Customization

- **Change Model:** Update model loading and prediction logic in `main.py` to use a different forecasting model.
- **Add Features:** Extend the data file and visualization code to include more features (e.g., volume, open/high/low prices).

---

## License

This project is for educational and demonstration purposes.

---

## Author

Your Name
