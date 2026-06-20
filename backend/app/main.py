from datetime import date
import json

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.schemas.backtest import (
    BacktestRequest,
    BacktestResponse,
    RebalanceFrequency,
    WeightingMethod,
)
from app.services.load_data import load_stock_data
from app.services.backtest_engine import run_backtest
from app.services.metrics_engine import build_backtest_insights, calculate_metrics


app = FastAPI(
    title="Qode Backtesting Platform",
    description="Backtesting API for strategy selection, portfolio construction, and result inspection.",
    version="1.0.0",
    json_encoders={date: lambda v: v.isoformat()}
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error: {str(exc)}"},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )


@app.get("/")
def home():
    return {
        "message": "Qode Backtesting Platform API",
        "docs": "/docs",
        "health": "/health",
        "backtest_post": "/backtest",
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


def _run_backtest(request: BacktestRequest) -> BacktestResponse:
    try:
        data = load_stock_data()
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to load stock data: {str(exc)}"
        ) from exc

    try:
        result = run_backtest(
            data=data,
            start_date=request.start_date,
            end_date=request.end_date,
            initial_capital=request.initial_capital,
            rebalance_frequency=request.rebalance_frequency,
            portfolio_size=request.portfolio_size,
            weighting_method=request.weighting_method,
            min_roe=request.min_roe,
            max_pe=request.max_pe,
            min_market_cap=request.min_market_cap,
            max_market_cap=request.max_market_cap,
            ranking_metric=request.ranking_metric,
            ranking_metrics=request.ranking_metrics,
            ranking_ascending=request.ranking_ascending,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    if result.empty:
        return BacktestResponse(
            parameters=request,
            metrics=calculate_metrics(result),
            rebalance_summary=[],
            equity_curve=[],
            drawdown_curve=[],
            top_winners=[],
            top_losers=[],
            records=[],
            total_records=0,
        )

    # Convert records and ensure dates are ISO format strings
    records = result.to_dict(orient="records")
    records = [
        {
            k: (v.isoformat() if hasattr(v, "isoformat") else v)
            for k, v in record.items()
        }
        for record in records
    ]
    
    metrics = calculate_metrics(result)
    insights = build_backtest_insights(result)

    return BacktestResponse(
        parameters=request,
        metrics=metrics,
        rebalance_summary=insights["rebalance_summary"],
        equity_curve=insights["equity_curve"],
        drawdown_curve=insights["drawdown_curve"],
        top_winners=insights["top_winners"],
        top_losers=insights["top_losers"],
        records=records,
        total_records=len(records),
    )


@app.get("/backtest", response_model=BacktestResponse)
def backtest_get(
    start_date: date = Query(default=date(2024, 1, 1)),
    end_date: date = Query(default=date(2025, 12, 31)),
    initial_capital: int = Query(default=1_000_000, gt=0),
    rebalance_frequency: RebalanceFrequency = Query(default="monthly"),
    portfolio_size: int = Query(default=3, gt=0, le=50),
    weighting_method: WeightingMethod = Query(default="equal"),
    min_roe: float | None = Query(default=None),
    max_pe: float | None = Query(default=None),
    min_market_cap: float | None = Query(default=None),
    max_market_cap: float | None = Query(default=None),
    ranking_metric: str = Query(default="roe"),
    ranking_metrics: list[str] | None = Query(default=None),
    ranking_ascending: bool = Query(default=False),
):
    request = BacktestRequest(
        start_date=start_date,
        end_date=end_date,
        initial_capital=initial_capital,
        rebalance_frequency=rebalance_frequency,
        portfolio_size=portfolio_size,
        weighting_method=weighting_method,
        min_roe=min_roe,
        max_pe=max_pe,
        min_market_cap=min_market_cap,
        max_market_cap=max_market_cap,
        ranking_metric=ranking_metric,
        ranking_metrics=ranking_metrics,
        ranking_ascending=ranking_ascending,
    )

    return _run_backtest(request)


@app.post("/backtest", response_model=BacktestResponse)
def backtest_post(request: BacktestRequest):
    return _run_backtest(request)
