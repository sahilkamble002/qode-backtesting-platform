# Architecture Overview

## High-Level Flow

1. Price history is stored in `stock_prices`.
2. Fundamental snapshots are stored in `financial_metrics` with `report_date`.
3. Detailed financial statements are stored in:
   - `profit_loss_statements`
   - `balance_sheet_statements`
   - `cash_flow_statements`
4. The backend loads price data for the requested date range.
5. For each rebalance period, the engine:
   - Finds the period entry date
   - Loads only fundamentals known on or before that date
   - Filters the current universe
   - Ranks the filtered stocks
   - Builds the portfolio
6. Metrics and dashboard insight series are returned to the frontend.
7. The frontend renders charts, tables, movers, and exports.

## No-Lookahead Design

The core anti-leakage rule is:

```text
report_date <= rebalance_date
```

`select_stocks()` now accepts `rebalance_date` and loads the latest available snapshot per symbol up to that date. This prevents future fundamentals from influencing earlier portfolio decisions.

## Backend Layers

- `app/main.py`: FastAPI endpoints and request/response orchestration
- `app/schemas/backtest.py`: API request and response contracts
- `app/models/*.py`: SQLAlchemy table definitions
- `app/services/backtest_engine.py`: rebalance loop and portfolio construction
- `app/services/strategy_engine.py`: historical fundamentals loading and stock selection
- `app/services/filter_engine.py`: fundamental filters
- `app/services/ranking_engine.py`: single-metric and composite ranking
- `app/services/metrics_engine.py`: performance metrics, equity curve, drawdown, movers
- `app/services/fundamental_fetcher.py`: yfinance-based fundamentals and statements ingestion

## Frontend Layers

- `src/App.jsx`: app-level state, API calls, exports
- `src/components/forms/BacktestForm.jsx`: parameter input UI
- `src/components/dashboard/*.jsx`: metrics, charts, tables, movers, empty states
- `src/lib/api.js`: payload normalization and API requests
- `src/styles.css`: Tailwind import and shared theme primitives

## Database Tables

### `stock_prices`

- `symbol`
- `date`
- `open`
- `high`
- `low`
- `close`
- `volume`

### `financial_metrics`

- `symbol`
- `report_date`
- `market_cap`
- `pe`
- `roe`
- `roce`
- `pat`
- `debt_to_equity`
- `current_ratio`
- `last_updated`

### `profit_loss_statements`

- `symbol`
- `report_date`
- `revenue`
- `ebit`
- `pretax_income`
- `net_income`
- `eps`

### `balance_sheet_statements`

- `symbol`
- `report_date`
- `total_assets`
- `total_liabilities`
- `total_equity`
- `current_assets`
- `current_liabilities`
- `cash_and_equivalents`
- `total_debt`
- `capital_employed`

### `cash_flow_statements`

- `symbol`
- `report_date`
- `operating_cash_flow`
- `investing_cash_flow`
- `financing_cash_flow`
- `capital_expenditure`
- `free_cash_flow`
