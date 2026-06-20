import unittest
from unittest.mock import patch

import pandas as pd

from app.services.data_fetcher import fetch_stock_data


class FetchStockDataTests(unittest.TestCase):
    @patch("app.services.data_fetcher.STOCKS", ["AAA.NS", "BBB.NS"])
    @patch("app.services.data_fetcher.yf.download")
    def test_fetch_stock_data_combines_symbols(self, mock_download):
        def fake_download(*args, **kwargs):
            return pd.DataFrame(
                {
                    "Date": pd.to_datetime(["2024-01-01", "2024-01-02"]),
                    "Open": [100.0, 101.0],
                    "High": [102.0, 103.0],
                    "Low": [99.0, 100.0],
                    "Close": [101.0, 102.0],
                    "Volume": [1000, 1200],
                }
            )

        mock_download.side_effect = fake_download

        result = fetch_stock_data()

        self.assertFalse(result.empty)
        self.assertIn("symbol", result.columns)
        self.assertEqual(set(result["symbol"]), {"AAA.NS", "BBB.NS"})


if __name__ == "__main__":
    unittest.main()
