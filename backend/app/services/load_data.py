
import pandas as pd

from sqlalchemy import text

from app.database import engine


def load_stock_data():

    query = text(
        """
        SELECT
            symbol,
            date,
            open,
            high,
            low,
            close,
            volume

        FROM stock_prices
        """
    )

    with engine.connect() as conn:

        df = pd.read_sql(
            query,
            conn
        )

    df["date"] = pd.to_datetime(
        df["date"]
    )

    return df