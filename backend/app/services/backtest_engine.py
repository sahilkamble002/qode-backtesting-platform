import pandas as pd

from app.services.strategy_engine import select_stocks

from app.services.portfolio_engine import (
    equal_weight_portfolio,
    market_cap_weight_portfolio,
    metric_weight_portfolio
)


def _build_period_frame(period_data):
    ordered = period_data.sort_values("date")

    entry = (
        ordered
        .groupby("symbol", as_index=False)
        .first()
        .rename(
            columns={
                "date": "entry_date",
                "open": "entry_open",
                "high": "entry_high",
                "low": "entry_low",
                "close": "entry_close",
                "volume": "entry_volume",
            }
        )
    )

    exit_frame = (
        ordered
        .groupby("symbol", as_index=False)
        .last()
        .rename(
            columns={
                "date": "exit_date",
                "open": "exit_open",
                "high": "exit_high",
                "low": "exit_low",
                "close": "exit_close",
                "volume": "exit_volume",
            }
        )
    )

    return entry.merge(
        exit_frame,
        on="symbol",
        how="inner",
    )


def run_backtest(
    data,
    start_date,
    end_date,
    initial_capital=1000000,
    rebalance_frequency="monthly",
    portfolio_size=3,
    weighting_method="equal",
    min_roe=None,
    max_pe=None,
    min_market_cap=None,
    max_market_cap=None,
    ranking_metric="roe",
    ranking_metrics=None,
    ranking_ascending=False,
):

    data = data.copy()
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    data = data[

        (data["date"] >= start_date)

        &

        (data["date"] <= end_date)

    ]

    # Rebalancing periods

    if rebalance_frequency == "monthly":

        data["period"] = data["date"].dt.to_period("M")

    elif rebalance_frequency == "quarterly":

        data["period"] = data["date"].dt.to_period("Q")

    else:

        data["period"] = data["date"].dt.to_period("Y")

    portfolio_log = []

    current_capital = initial_capital

    for period in data["period"].unique():

        period_data = data[

            data["period"] == period

        ]

        period_frame = _build_period_frame(period_data)
        rebalance_date = period_frame["entry_date"].min()

        strategy_data = select_stocks(
            portfolio_size=portfolio_size,
            min_roe=min_roe,
            max_pe=max_pe,
            min_market_cap=min_market_cap,
            max_market_cap=max_market_cap,
            ranking_metric=ranking_metric,
            ranking_metrics=ranking_metrics,
            ranking_ascending=ranking_ascending,
            universe_symbols=period_frame["symbol"].dropna().unique().tolist(),
            rebalance_date=rebalance_date,
        )

        if strategy_data.empty:
            continue

        selected_symbols = strategy_data[

            "symbol"

        ].tolist()

        selected = period_frame[

            period_frame["symbol"].isin(

                selected_symbols

            )

        ]

        selected = selected.merge(

            strategy_data,

            on="symbol",

            how="left"

        )

        if selected.empty:
            continue

        if weighting_method == "equal":

            portfolio = equal_weight_portfolio(

                selected,

                current_capital,
                price_column="entry_close"

            )

        elif weighting_method == "market_cap":

            portfolio = market_cap_weight_portfolio(

                selected,

                current_capital,
                price_column="entry_close"

            )

        else:

            portfolio = metric_weight_portfolio(

                selected,

                current_capital,

                metric="roe",
                price_column="entry_close"

            )

        portfolio["capital_start"] = current_capital
        portfolio["exit_value"] = portfolio["shares"] * portfolio["exit_close"]
        portfolio["profit_loss"] = (
            portfolio["exit_value"] - portfolio["allocation"]
        )
        portfolio["return_pct"] = (
            portfolio["profit_loss"] / portfolio["allocation"]
        )
        portfolio["period_start"] = portfolio["entry_date"]
        portfolio["period_end"] = portfolio["exit_date"]
        portfolio["rebalance_date"] = pd.to_datetime(rebalance_date).date().isoformat()
        portfolio["period_portfolio_value"] = portfolio["exit_value"].sum()
        portfolio["capital_end"] = portfolio["period_portfolio_value"]

        current_capital = float(
            portfolio["period_portfolio_value"].iloc[0]
        )

        if "period" in portfolio.columns:
            portfolio = portfolio.drop(
                columns=["period"]
            )

        portfolio_log.append(

            portfolio

        )

    if not portfolio_log:
        return pd.DataFrame()

    return pd.concat(

        portfolio_log,

        ignore_index=True

    )
