import math

import pandas as pd


def _build_rebalance_summary(portfolio):
    summary = (
        portfolio.groupby("rebalance_date", as_index=False)
        .agg(
            period_start=("period_start", "first"),
            period_end=("period_end", "first"),
            capital_start=("capital_start", "first"),
            capital_end=("capital_end", "first"),
            period_return=("return_pct", "mean"),
            positions=("symbol", "count"),
        )
        .sort_values("period_start")
        .reset_index(drop=True)
    )

    summary["drawdown"] = (
        summary["capital_end"] / summary["capital_end"].cummax()
    ) - 1

    return summary


def build_backtest_insights(portfolio):
    if portfolio.empty:
        return {
            "rebalance_summary": [],
            "equity_curve": [],
            "drawdown_curve": [],
            "top_winners": [],
            "top_losers": [],
        }

    summary = _build_rebalance_summary(portfolio)

    equity_curve = [
        {
            "rebalance_date": row["rebalance_date"],
            "period_start": row["period_start"].isoformat() if hasattr(row["period_start"], "isoformat") else str(row["period_start"]),
            "period_end": row["period_end"].isoformat() if hasattr(row["period_end"], "isoformat") else str(row["period_end"]),
            "capital_start": float(row["capital_start"]),
            "capital_end": float(row["capital_end"]),
            "period_return_pct": float(row["period_return"] * 100),
        }
        for _, row in summary.iterrows()
    ]

    drawdown_curve = [
        {
            "rebalance_date": row["rebalance_date"],
            "period_start": row["period_start"].isoformat() if hasattr(row["period_start"], "isoformat") else str(row["period_start"]),
            "period_end": row["period_end"].isoformat() if hasattr(row["period_end"], "isoformat") else str(row["period_end"]),
            "drawdown_pct": float(row["drawdown"] * 100),
        }
        for _, row in summary.iterrows()
    ]

    grouped_positions = (
        portfolio.groupby("symbol", as_index=False)
        .agg(
            total_profit_loss=("profit_loss", "sum"),
            average_return_pct=("return_pct", "mean"),
            times_selected=("symbol", "count"),
        )
        .sort_values("total_profit_loss", ascending=False)
        .reset_index(drop=True)
    )

    top_winners = grouped_positions.head(5).to_dict(orient="records")
    top_losers = (
        grouped_positions.tail(5)
        .sort_values("total_profit_loss")
        .to_dict(orient="records")
    )

    # Convert rebalance_summary with date conversion
    rebalance_summary = []
    for _, row in summary.iterrows():
        rebalance_summary.append({
            "rebalance_date": row["rebalance_date"],
            "period_start": row["period_start"].isoformat() if hasattr(row["period_start"], "isoformat") else str(row["period_start"]),
            "period_end": row["period_end"].isoformat() if hasattr(row["period_end"], "isoformat") else str(row["period_end"]),
            "capital_start": float(row["capital_start"]),
            "capital_end": float(row["capital_end"]),
            "period_return": float(row["period_return"]),
            "positions": int(row["positions"]),
            "drawdown": float(row["drawdown"]),
        })

    return {
        "rebalance_summary": rebalance_summary,
        "equity_curve": equity_curve,
        "drawdown_curve": drawdown_curve,
        "top_winners": top_winners,
        "top_losers": top_losers,
    }


def calculate_metrics(portfolio):
    if portfolio.empty:
        return {
            "portfolio_entries": 0,
            "unique_stocks_selected": 0,
            "total_allocation": 0.0,
            "initial_capital": 0.0,
            "final_capital": 0.0,
            "total_return_pct": 0.0,
            "cagr_pct": 0.0,
            "max_drawdown_pct": 0.0,
            "volatility_pct": 0.0,
            "sharpe_ratio": 0.0,
            "winning_periods": 0,
            "losing_periods": 0,
            "number_of_rebalances": 0,
        }

    summary = _build_rebalance_summary(portfolio)

    initial_capital = float(summary["capital_start"].iloc[0])
    final_capital = float(summary["capital_end"].iloc[-1])
    total_return_pct = (
        ((final_capital - initial_capital) / initial_capital) * 100
        if initial_capital
        else 0.0
    )

    start_date = pd.to_datetime(summary["period_start"].iloc[0])
    end_date = pd.to_datetime(summary["period_end"].iloc[-1])
    total_days = max((end_date - start_date).days, 1)
    years = total_days / 365.25

    if initial_capital > 0 and final_capital > 0 and years > 0:
        cagr_pct = ((final_capital / initial_capital) ** (1 / years) - 1) * 100
    else:
        cagr_pct = 0.0

    period_returns = summary["period_return"].fillna(0.0)
    volatility_pct = float(period_returns.std(ddof=0) * 100) if len(period_returns) > 1 else 0.0

    if len(period_returns) > 1 and period_returns.std(ddof=0) != 0:
        sharpe_ratio = float(
            (period_returns.mean() / period_returns.std(ddof=0)) * math.sqrt(len(period_returns))
        )
    else:
        sharpe_ratio = 0.0

    return {
        "portfolio_entries": int(len(portfolio)),
        "unique_stocks_selected": int(portfolio["symbol"].nunique()),
        "total_allocation": float(portfolio["allocation"].sum()),
        "initial_capital": initial_capital,
        "final_capital": final_capital,
        "total_return_pct": float(total_return_pct),
        "cagr_pct": float(cagr_pct),
        "max_drawdown_pct": float(summary["drawdown"].min() * 100),
        "volatility_pct": float(volatility_pct),
        "sharpe_ratio": float(sharpe_ratio),
        "winning_periods": int((summary["period_return"] > 0).sum()),
        "losing_periods": int((summary["period_return"] < 0).sum()),
        "number_of_rebalances": int(len(summary)),
    }
