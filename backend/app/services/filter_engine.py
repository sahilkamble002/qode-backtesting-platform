def filter_stocks(
    data,
    min_roe=None,
    max_pe=None,
    min_market_cap=None,
    max_market_cap=None,
):
    filtered = data.copy()

    if min_roe is not None:
        filtered = filtered[
            filtered["roe"] >= min_roe
        ]

    if max_pe is not None:
        filtered = filtered[
            filtered["pe"] <= max_pe
        ]

    if min_market_cap is not None:
        filtered = filtered[
            filtered["market_cap"] >= min_market_cap
        ]

    if max_market_cap is not None:
        filtered = filtered[
            filtered["market_cap"] <= max_market_cap
        ]

    filtered = filtered.dropna(
        subset=["symbol"]
    )

    return filtered.reset_index(
        drop=True
    )
