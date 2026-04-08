# Rami Al Stocks (رامي السهم) 📈

Arabic-first Streamlit app for analyzing Saudi stocks (Tadawul) using price behavior, yearly trend, and Bollinger Bands.

## Overview

`Rami Al Stocks` helps traders and investors quickly evaluate Saudi equities by combining:

- live market data from Yahoo Finance (`yfinance`)
- yearly moving average context (long-term trend)
- Bollinger channel position (possible rebound/overextension zones)
- clear recommendation cards and watchlist navigation

The interface is optimized for Arabic users and includes right-to-left layout support.

## Key Features

- **Arabic-first UI (RTL):** Designed for Arabic readability and workflow.
- **Smart recommendation engine:** Classifies stock state (e.g., buy/hold/watch/sell) based on indicator logic.
- **Sidebar watchlist:** Browse major Tadawul stocks from a prepared list.
- **Stock analysis panel:** Current price, yearly average, and indicator-based guidance.
- **Interactive chart:** Plotly chart for price history and indicator bands.
- **Dividend badge:** Shows when a stock has dividend distribution history.

## Tech Stack

- **App framework:** Streamlit
- **Data source:** yfinance
- **Data processing:** pandas, numpy
- **Visualization:** Plotly
- **Language:** Python 3.12+

## Project Structure

```text
.
├── main.py            # Main Streamlit application
├── requirements.txt   # Python dependencies
├── run_app.sh         # Helper script to run app locally
└── README.md
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/AHNEMER/rami-Al-stocks.git
cd rami-Al-stocks
```

2. Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run Locally

Recommended:

```bash
streamlit run main.py
```

Or with Python module:

```bash
python -m streamlit run main.py
```

Then open the local URL shown in terminal (usually `http://localhost:8501`).

## Usage

- Select a stock from the sidebar watchlist.
- Review recommendation card and technical summary.
- Inspect chart behavior around yearly average and Bollinger boundaries.
- Use signals as decision support, not as guaranteed trading advice.

## Important Notes

- Market data is fetched from Yahoo Finance and may occasionally be delayed or unavailable.
- The app is intended for educational and decision-support use.
- Not financial advice.

## Troubleshooting

- **App does not start:** Make sure virtual environment is activated and dependencies are installed.
- **No data returned for a symbol:** Try again later or test another ticker.
- **Module import errors:** Re-run `pip install -r requirements.txt`.

## GitHub Publishing Checklist

- Ensure `venv/` is excluded in `.gitignore` (already included).
- Commit only source files and config files (not local environments).
- Add screenshots to this README (recommended) for better presentation.

## Roadmap Ideas

- Add multilingual toggle (Arabic/English).
- Add unit tests for recommendation logic.
- Add export options for analysis snapshots.
- Add optional alerts and watchlist persistence.

## License

Choose and add a license file (for example, MIT) before public release.

