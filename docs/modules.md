# Module Guide

## Backend

### `app/services/backtest_engine.py`

- Builds rebalance periods from price data
- Re-runs `select_stocks()` inside each period
- Merges selected fundamentals with price entry/exit rows
- Calculates realized P&L and capital progression

### `app/services/strategy_engine.py`

- Loads financial metrics from the database
- Applies `report_date <= rebalance_date`
- Keeps the most recent known snapshot per symbol
- Applies filters and ranking

### `app/services/filter_engine.py`

Supported filters:

- `min_roe`
- `max_pe`
- `min_market_cap`
- `max_market_cap`

### `app/services/ranking_engine.py`

Supports:

- Single-metric ranking
- Composite ranking from multiple metrics
- Average-rank scoring across selected metrics

### `app/services/fundamental_fetcher.py`

Fetches:

- Ratios from `stock.info`
- Income statement rows
- Balance sheet rows
- Cash flow rows

Computes:

- `pat` from net income
- `roce` from `EBIT / Capital Employed`
- `free_cash_flow` from operating cash flow and capex

### `app/services/metrics_engine.py`

Returns:

- Summary metrics
- Rebalance summary
- Equity curve data
- Drawdown curve data
- Top winners
- Top losers

## Frontend

### `src/App.jsx`

- Manages API state
- Validates inputs
- Triggers backtests
- Exports CSV/Excel files

### `src/components/forms/BacktestForm.jsx`

- Date, capital, rebalance, and weighting inputs
- Fundamental filters
- Market-cap range inputs
- Composite metric selection

### `src/components/dashboard/EquityCurve.jsx`

- Renders the equity curve
- Renders the drawdown chart
- Uses Recharts

### `src/components/dashboard/RebalanceSummary.jsx`

- Tabular period-by-period summary
- Includes drawdown visibility

### `src/components/dashboard/TopMovers.jsx`

- Summarizes best and worst contributors by aggregated P&L

### `src/components/dashboard/PositionsTable.jsx`

- Displays position-level output
- Includes `report_date` for transparency on which fundamentals were used
