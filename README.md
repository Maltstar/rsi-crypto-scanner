# RSI Crypto Scanner

Fetches RSI (Relative Strength Index) values for the top 1000 cryptocurrencies by CoinMarketCap ranking, using the Polygon.io API. Results are saved as CSV files in the `gen/` folder.

## What it does

- Retrieves the top 1000 cryptos ranked by CoinMarketCap
- Matches each crypto symbol to its trading pairs on Polygon.io
- Fetches two RSI values per ticker: **21-day** and **210-day** (daily close)
- Outputs two CSV files:
  - `gen/RSI_records-<date>_gen.csv` — successful RSI records
  - `gen/RSI_exceptions-<date>.csv` — tickers for which RSI could not be retrieved

## Prerequisites

- Python 3.8+
- A [CoinMarketCap API key](https://coinmarketcap.com/api/)
- A [Polygon.io API key](https://polygon.io/)

## Installation

### 1. Create and activate a virtual environment

```bash
cd rsi_new
python3 -m venv src/venv
source src/venv/bin/activate
```

On Windows:
```bash
src\venv\Scripts\activate
```

### 2. Install the required dependencies

```bash
pip install polygon-api-client python-dotenv pandas requests
```

## Configuration

Create a `.env` file at the project root (next to the `src/` folder) with your API keys:

```
CMC_PRO_API_KEY=your_coinmarketcap_api_key
CMC_PRO_URL=https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest
POL_API_KEY=your_polygon_api_key
```

## Project structure

```
rsi_new/
├── .env                  # API keys (not committed)
├── src/                  # Source scripts
│   ├── venv/             # Virtual environment
│   ├── get_rsi.py        # Main entry point
│   ├── polygon_api.py    # Polygon.io API wrapper
│   ├── get_cryptos_by_ranking.py  # CoinMarketCap API wrapper
│   ├── reduce_tickers_by_ranking.py
│   └── local_api.py      # Path helpers and utilities
├── db/                   # Input CSV databases
└── gen/                  # Generated output files (created at runtime)
```

## How to run

### 1. Activate the virtual environment

From the project root:

```bash
source src/venv/bin/activate
```

On Windows:
```bash
src\venv\Scripts\activate
```

### 2. Run the script

The script must be run from the `src/` directory so that relative imports resolve correctly:

```bash
cd src
python get_rsi.py
```

To run it in the background and keep a log (recommended given the long runtime):

```bash
cd src
nohup python get_rsi.py > ../get_rsi_run.log 2>&1 &
```

Monitor progress:
```bash
grep "\[API request" ../get_rsi_run.log | tail -3
```

The script will print progress to the console, including the start time, each ticker being processed, and a summary at the end.

> **Note:** The free Polygon.io tier allows 5 API calls per minute. The script adds a 12-second delay between each call automatically to stay within this limit. Scanning 1000 cryptos (2 RSI calls each) takes approximately **4–5 hours**.

## Output format

`RSI_records-<date>_gen.csv` columns:

| Column | Description |
|--------|-------------|
| description | Full name of the crypto |
| ticker | Trading pair (e.g. `BTCUSDT`) |
| RSI 1D (210-day) | RSI with a 210-day window |
| RSI 1D (21-day) | RSI with a 21-day window |
| cmc_rank | CoinMarketCap ranking |
| date and time | Timestamp of the RSI data point |
