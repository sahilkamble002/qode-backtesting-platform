from datetime import date
from typing import Literal
from pydantic import BaseModel, Field, model_validator

RebalanceFrequency = Literal["monthly", "quarterly", "yearly"]
WeightingMethod = Literal["equal", "market_cap", "metric"]
class BacktestRequest(BaseModel):
    start_date: date = Field(default=date(2024, 1, 1))
    end_date: date = Field(default=date(2025, 12, 31))
    initial_capital: int = Field(default=1_000_000, gt=0)
    rebalance_frequency: RebalanceFrequency = "monthly"
    portfolio_size: int = Field(default=3, gt=0, le=50)
    weighting_method: WeightingMethod = "equal"
    min_roe: float | None = None
    max_pe: float | None = None
    min_market_cap: float | None = None
    max_market_cap: float | None = None
    ranking_metric: str = "roe"
    ranking_metrics: list[str] | None = None
    ranking_ascending: bool = False

    @model_validator(mode="after")
    def validate_date_range(self):
        if self.start_date > self.end_date:
            raise ValueError("start_date must be before or equal to end_date")
        allowed_metrics = {"roe", "pe", "market_cap", "roce", "pat", "debt_to_equity", "current_ratio"}
        if self.ranking_metric not in allowed_metrics:
            raise ValueError("ranking_metric must be one of: roe, pe, market_cap, roce, pat, debt_to_equity, current_ratio")
        if self.ranking_metrics:
            invalid_metrics = sorted(set(self.ranking_metrics) - allowed_metrics)
            if invalid_metrics:
                raise ValueError(
                    "ranking_metrics contains invalid values: " + ", ".join(invalid_metrics)
                )
        return self
class BacktestPosition(BaseModel):
    symbol: str
    entry_date: date
    entry_open: float
    entry_high: float
    entry_low: float
    entry_close: float
    entry_volume: float
    exit_date: date
    exit_open: float
    exit_high: float
    exit_low: float
    exit_close: float
    exit_volume: float
    roe: float | None = None
    pe: float | None = None
    market_cap: float | None = None
    report_date: date | None = None
    weight: float
    allocation: float
    shares: float
    portfolio_value: float
    exit_value: float
    profit_loss: float
    return_pct: float
    capital_start: float
    capital_end: float
    period_portfolio_value: float
    period_start: date
    period_end: date
    rebalance_date: str
class BacktestMetrics(BaseModel):
    portfolio_entries: int
    unique_stocks_selected: int
    total_allocation: float
    initial_capital: float
    final_capital: float
    total_return_pct: float
    cagr_pct: float
    max_drawdown_pct: float
    volatility_pct: float
    sharpe_ratio: float
    winning_periods: int
    losing_periods: int
    number_of_rebalances: int
class RebalanceSummaryPoint(BaseModel):
    rebalance_date: str
    period_start: date
    period_end: date
    capital_start: float
    capital_end: float
    period_return: float
    positions: int
    drawdown: float
class EquityCurvePoint(BaseModel):
    rebalance_date: str
    period_start: date
    period_end: date
    capital_start: float
    capital_end: float
    period_return_pct: float
class DrawdownPoint(BaseModel):
    rebalance_date: str
    period_start: date
    period_end: date
    drawdown_pct: float
class TopMover(BaseModel):
    symbol: str
    total_profit_loss: float
    average_return_pct: float
    times_selected: int
class BacktestResponse(BaseModel):
    parameters: BacktestRequest
    metrics: BacktestMetrics
    rebalance_summary: list[RebalanceSummaryPoint] = []
    equity_curve: list[EquityCurvePoint] = []
    drawdown_curve: list[DrawdownPoint] = []
    top_winners: list[TopMover] = []
    top_losers: list[TopMover] = []
    records: list[BacktestPosition]
    total_records: int
