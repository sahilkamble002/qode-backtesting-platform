# Qode Backtesting Platform

This project is a full-stack stock backtesting platform with a FastAPI backend and a Vite + React frontend. It now supports dynamic rebalancing, dated fundamentals with no future-data leakage, composite multi-metric ranking, market-cap range filters, chart-based analytics, and CSV/Excel exports.

## Tech Stack

- Backend: FastAPI, SQLAlchemy, pandas, yfinance, PostgreSQL
- Frontend: React 19, Vite 7, Tailwind CSS 4, Recharts, SheetJS

## Project Structure

```text
backend/
  app/
    main.py
    database.py
    models/
    schemas/
    services/
  create_tables.py
  insert_data.py
  insert_fundamentals.py
  test_*.py
frontend/
  src/
    components/
    lib/
    App.jsx
  package.json
docs/
  architecture.md
  modules.md
  assumptions.md
```

## Backend Setup

1. Create a PostgreSQL database.
2. Set backend environment variables in `backend/.env`:

```env
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=qode_backtesting
```

3. Create tables:

```bash
cd backend
venv\Scripts\python.exe create_tables.py
```

4. Load price data:

```bash
venv\Scripts\python.exe insert_data.py
```

5. Load dated fundamentals and financial statements:

```bash
venv\Scripts\python.exe insert_fundamentals.py
```

6. Start the API:

```bash
venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

API docs will be available at `http://127.0.0.1:8000/docs`.

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The frontend runs on `http://127.0.0.1:5173` and proxies `/backtest` and `/health` to the backend.

## Running Tests

Backend test suite:

```bash
cd ..
backend\venv\Scripts\python.exe -m unittest discover -s backend -p "test_*.py"
```

Frontend production build:

```bash
cd frontend
npm run build
```

## Key Features

- Dynamic stock selection on every rebalance period
- Historical fundamentals filtered with `report_date <= rebalance_date`
- Market-cap min/max filters
- Composite ranking across multiple metrics
- P&L, Balance Sheet, and Cash Flow statement storage
- Equity curve and drawdown charts
- Top winners and top losers views
- CSV and Excel export
- Tailwind CSS based UI

## Important Notes

- `yfinance` statement labels can vary between tickers, so some fields may be `null` when Yahoo does not expose them.
- `marketCap`, `trailingPE`, and some ratios come from the latest available `info` payload, while PAT/ROCE and statements are built from dated financial statements.
- The frontend build currently passes, but Vite reports a large bundle warning because `xlsx` is included in the main bundle. This is a performance warning, not a build failure.

More detail is available in `docs/architecture.md`, `docs/modules.md`, and `docs/assumptions.md`.
