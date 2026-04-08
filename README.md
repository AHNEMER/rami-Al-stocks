# Rami Al Stocks (رامي السهم) 📈

Arabic-first Streamlit app for analyzing Saudi stocks (Tadawul) using price behavior, yearly trend, and Bollinger Bands.

## Overview

`Rami Al Stocks` helps traders and investors quickly evaluate Saudi equities by combining:

- Live market data from Yahoo Finance (`yfinance`) with advanced rate-limit bypassing.
- Yearly moving average context (long-term trend).
- Bollinger channel position (possible rebound/overextension zones).
- Clear recommendation cards and watchlist navigation.

The interface is optimized for Arabic users and includes right-to-left layout support. It is built to seamlessly deploy and run smoothly on **Streamlit Community Cloud**.

## Key Features

- **Arabic-first UI (RTL):** Designed for Arabic readability and workflow.
- **Smart recommendation engine:** Classifies stock state (e.g., buy/hold/watch/sell) based on indicator logic.
- **Sidebar watchlist:** Browse major Tadawul stocks from a prepared list.
- **Stock analysis panel:** Current price, yearly average, and indicator-based guidance.
- **Interactive chart:** Plotly chart for price history and indicator bands.
- **Resilient Data Fetching:** Built-in exponential backoffs and 24-hour intelligent caching to effortlessly bypass Yahoo Finance rate limits.

## Tech Stack

- **App framework:** Streamlit
- **Data source:** yfinance (v1.2.1+) & curl_cffi
- **Data processing:** pandas, pandas-ta
- **Visualization:** Plotly
- **Language:** Python 3.12 (Strictly Recommended)

## Project Structure

```text
.
├── main.py            # Main Streamlit application
├── requirements.txt   # Python dependencies 
├── run_app.sh         # Helper script to run app locally
└── README.md
```

## Cloud Deployment (Streamlit Community Cloud)

If you are deploying this app to Streamlit Community Cloud, **you must follow these specific steps** to avoid endless builds and rate limits:

1. Connect your GitHub repository to Streamlit Cloud.
2. Under your App Settings on Streamlit Cloud, go to **Advanced** settings.
3. Change the **Python Version** to `3.12`. 
   > *Note: If you use higher experimental versions (like 3.14), the app will take over 20 minutes to compile because `pandas` and other libraries will need to be built from scratch without pre-compiled wheels.*
4. Deploy the app. The optimized `requirements.txt` will instantly fetch lightweight dependencies.

## Installation & Local Run

1. Clone the repository:

```bash
git clone https://github.com/AHNEMER/rami-Al-stocks.git
cd rami-Al-stocks
```

2. Create and activate a virtual environment (using Python 3.12):

```bash
python3.12 -m venv venv
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the app:

```bash
streamlit run main.py
```
Then open the local URL shown in terminal (usually `http://localhost:8501`).

## Troubleshooting

- **YFRateLimitError (Too Many Requests):** Handled natively by the app via `curl_cffi` backend and exponential backoff loops. If it still occurs, wait 2-3 minutes. The data leverages a 24-hour cache limit.
- **App taking forever to deploy on Cloud:** Check your Python version. Ensure it is set exactly to `3.12` in the Cloud settings.
- **YFDataException or Compatibility issues:** Ensure `curl_cffi` is in your `requirements.txt` and you are using `yfinance>=1.2.1`.

## License

This project is open for educational and decision-support use. Not financial advice.
