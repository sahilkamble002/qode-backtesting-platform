import pandas as pd

from sqlalchemy import text

from app.database import engine
from app.services.filter_engine import filter_stocks
from app.services.ranking_engine import rank_stocks


def load_financial_metrics(as_of_date=None):
    where_clause = ""
    query_params = {}

    if as_of_date is not None:
        where_clause = "WHERE report_date <= :as_of_date"
        query_params["as_of_date"] = pd.to_datetime(as_of_date).date()

    query = text("""

    SELECT

    symbol,
    report_date,

    roe,

    pe,

    market_cap,

    roce,

    pat,

    debt_to_equity,

    current_ratio

    FROM financial_metrics
    {where_clause}

    """.format(where_clause=where_clause))

    with engine.connect() as conn:

        data = pd.read_sql(
            query,
            conn,
            params=query_params
        )

    if data.empty:
        return data

    data["report_date"] = pd.to_datetime(data["report_date"])
    data = data.sort_values(["symbol", "report_date"])

    if as_of_date is not None:
        data = (
            data.groupby("symbol", as_index=False)
            .tail(1)
            .reset_index(drop=True)
        )

    return data


def select_stocks(
    portfolio_size=3,
    min_roe=None,
    max_pe=None,
    min_market_cap=None,
    max_market_cap=None,
    ranking_metric="roe",
    ranking_metrics=None,
    ranking_ascending=False,
    universe_symbols=None,
    rebalance_date=None,
):
    data = load_financial_metrics(as_of_date=rebalance_date)

    if universe_symbols is not None:
        data = data[
            data["symbol"].isin(universe_symbols)
        ]

    filtered = filter_stocks(
        data=data,
        min_roe=min_roe,
        max_pe=max_pe,
        min_market_cap=min_market_cap,
        max_market_cap=max_market_cap,
    )

    if filtered.empty:
        return filtered

    ranked = rank_stocks(
        data=filtered,
        metric=ranking_metric,
        metrics=ranking_metrics,
        ascending=ranking_ascending
    )

    return ranked.head(
        portfolio_size
    )
