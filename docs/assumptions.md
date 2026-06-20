# Assumptions and Limitations

## Data Assumptions

- Historical price data exists in `stock_prices`.
- Fundamental history is populated through `insert_fundamentals.py`.
- Financial statement dates coming from yfinance are treated as the report availability date.

## Practical Limitations

- Yahoo Finance does not always expose complete statement rows for every Indian ticker.
- Some ratio fields are current snapshots from `stock.info`, not reconstructed historical market snapshots.
- Exact filing-publication lag is not modeled; the current implementation uses statement `report_date` as the usable date boundary.

## Optional Enhancements

- Add a true filing-publication date if sourced from a filings provider or Screener.in.
- Store quarterly and annual statements separately.
- Add manual chunking or lazy loading for the Excel export path to reduce the frontend bundle size.
- Add migrations with Alembic instead of relying on `create_all()`.
- Add background ingestion jobs and retry handling for fundamentals scraping.
