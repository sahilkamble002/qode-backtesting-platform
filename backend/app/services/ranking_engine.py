def _validate_metric(data, metric):
    if metric not in data.columns:
        raise ValueError(
            f"Ranking metric '{metric}' not found in dataset"
        )


def rank_stocks(data, metric=None, metrics=None, ascending=False):
    metrics = metrics or ([metric] if metric else [])

    if not metrics:
        raise ValueError("At least one ranking metric is required")

    for current_metric in metrics:
        _validate_metric(data, current_metric)

    ranked = data.copy()

    if len(metrics) == 1:
        ranked = ranked.sort_values(
            by=metrics[0],
            ascending=ascending
        )
        return ranked.reset_index(drop=True)

    rank_columns = []
    for current_metric in metrics:
        rank_column = f"{current_metric}_rank"
        ranked[rank_column] = ranked[current_metric].rank(
            ascending=ascending,
            method="average",
            na_option="bottom"
        )
        rank_columns.append(rank_column)

    ranked["composite_rank"] = ranked[rank_columns].mean(axis=1)
    ranked = ranked.sort_values(
        by=["composite_rank"] + rank_columns,
        ascending=True
    )

    return ranked.reset_index(drop=True)
