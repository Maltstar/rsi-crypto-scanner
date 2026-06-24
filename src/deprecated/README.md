# Deprecated source files

These files are no longer used by the current main script (`get_rsi.py`) and have been moved here for reference. They fall into two categories: superseded code from an earlier version of the RSI pipeline, and standalone utility scripts that were part of a TradingView-based workflow that predates the Polygon.io migration.

---

## Superseded pipeline files

These files were part of the original RSI pipeline that used the TradingView TA library instead of the Polygon.io API. They have been replaced by `get_rsi.py`, `reduce_tickers_by_ranking.py`, and `polygon_api.py`.

### `get_rsi_old.py`
Previous version of the main RSI scanning script. It used the TradingView `TA_Handler` to fetch RSI values instead of the Polygon.io API. The list of cryptos to scan was built from TradingView screener data (via `reduce_screeners_by_ranking.py`) rather than from Polygon.io tickers. The file contains hardcoded test data (BTC/ETH/XRP repeated many times) left over from debugging.

### `reduce_screeners_by_ranking.py`
TradingView-based counterpart of `reduce_tickers_by_ranking.py`. It fetched the full list of crypto screeners from TradingView (via `update_crypto_screeners.py`) and filtered them down to the top N cryptos by CoinMarketCap rank. Superseded because the current pipeline sources tickers directly from the Polygon.io API.

### `update_crypto_screeners.py`
Fetched the complete list of crypto screeners from the TradingView scanner API (`https://scanner.tradingview.com/crypto/scan`). It was the data source for `reduce_screeners_by_ranking.py`. No longer needed since tickers now come from Polygon.io.

### `import_path.py`
Early version of the path configuration module, predating `local_api.py`. Defined the same `src_path_db`, `src_path_gen`, `src_path_usr` path variables but with different relative offsets (`../../` instead of `../`). Never imported by any other file; superseded by `local_api.py`.

### `test.py`
One-off script used to verify that Python's `pathlib.Path` resolved the correct absolute paths for the `db/` and `gen/` folders. No reusable logic; kept only as a path-debugging reference.

---

## Standalone utility scripts (TradingView workflow)

These scripts were used in a data preparation workflow that fed screener data into the old TradingView-based RSI pipeline. They are self-contained and each accepts a CSV file as a command-line argument.

### `check_positions.py`
Checks an open positions list against live TradingView data. For each position it fetches the 14-day RSI (daily interval) and the current price (1-minute interval), then calculates how far the current price is from the entry and stop-loss levels. Outputs two CSV files: one with all position details enriched with live data, and one with positions for which the TradingView fetch failed.

**Run:** `python check_positions.py <positions_file.csv>` (file must be in `usr/`)

### `extract_screeners.py`
Given a TradingView screener database CSV and a positions CSV, it looks up the screener entry (exchange + symbol + description) for each position symbol. Useful for converting a plain list of crypto symbols into the full format required by TradingView's `TA_Handler`. Outputs a matched screeners CSV and an exceptions CSV for symbols not found in the database.

**Run:** `python extract_screeners.py <db_screeners.csv> <positions_list.csv>`

### `extract_symbol_listing.py`
Extracts the ticker symbol from crypto listing files exported from LiveCoinWatch (LCW) or CoinMarketCap (CMCAP). Both sources bundle the symbol and the full name together in a single cell (e.g. `BitcoinBTC` or `BTCBitcoin`) with no delimiter, so this script uses regex pattern matching to split them. Outputs a CSV with a single `symbol` column.

**Run:** `python extract_symbol_listing.py <listing_file.csv>` (filename must contain `LCW` or `CMCAP` to select the correct parser)

### `little_tools.py`
Small helper module containing a single utility function `clean_csv(csv_in, column)` that removes a named column from a CSV file in-place using pandas. It was imported by `extract_screeners.py` and `get_rsi_old.py`, but the actual call to `clean_csv` in `extract_screeners.py` was commented out. Effectively unused.
