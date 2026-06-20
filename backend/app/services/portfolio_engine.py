import pandas as pd


def _finalize_portfolio(stocks_df, capital, price_column):
    if stocks_df.empty:
        return stocks_df.copy()

    if price_column not in stocks_df.columns:
        raise ValueError(
            f"Price column '{price_column}' not found in portfolio data"
        )

    stocks_df = stocks_df.copy()
    stocks_df["allocation"] = capital * stocks_df["weight"]
    stocks_df["shares"] = stocks_df["allocation"] / stocks_df[price_column]
    stocks_df["portfolio_value"] = stocks_df["shares"] * stocks_df[price_column]
    return stocks_df


def equal_weight_portfolio(stocks_df, capital, price_column="close"):

    stocks_df = stocks_df.copy()

    num_stocks = len(stocks_df)

    if num_stocks == 0:
        return stocks_df

    weight = 1 / num_stocks

    stocks_df["weight"] = weight
    return _finalize_portfolio(stocks_df, capital, price_column)


def market_cap_weight_portfolio(stocks_df, capital, price_column="close"):

    stocks_df = stocks_df.copy()

    if stocks_df.empty:
        return stocks_df

    total_market_cap = stocks_df["market_cap"].sum()

    if total_market_cap == 0:
        return equal_weight_portfolio(
            stocks_df,
            capital,
            price_column=price_column
        )

    stocks_df["weight"] = (

        stocks_df["market_cap"]

        /

        total_market_cap

    )
    return _finalize_portfolio(stocks_df, capital, price_column)


def metric_weight_portfolio(

    stocks_df,

    capital,

    metric="roe",
    price_column="close"

):

    stocks_df = stocks_df.copy()

    stocks_df[metric] = stocks_df[metric].fillna(0)

    total_metric = stocks_df[metric].sum()

    if total_metric == 0:

        return equal_weight_portfolio(

            stocks_df,

            capital,
            price_column=price_column

        )

    stocks_df["weight"] = (

        stocks_df[metric]

        /

        total_metric

    )
    return _finalize_portfolio(stocks_df, capital, price_column)
