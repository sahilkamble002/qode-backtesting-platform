import unittest
from unittest.mock import MagicMock, patch

import pandas as pd

from app.services.fundamental_fetcher import fetch_fundamentals


class FundamentalFetcherTests(unittest.TestCase):
    @patch("app.services.fundamental_fetcher.yf.Ticker")
    def test_fetch_fundamentals_maps_expected_fields(self, mock_ticker):
        mock_instance = MagicMock()
        mock_instance.info = {
            "marketCap": 1000000,
            "trailingPE": 15.5,
            "returnOnEquity": 0.22,
            "debtToEquity": 0.4,
            "currentRatio": 1.8,
        }
        mock_instance.income_stmt = pd.DataFrame(
            {
                pd.Timestamp("2024-03-31"): {
                    "Total Revenue": 500.0,
                    "EBIT": 120.0,
                    "Pretax Income": 110.0,
                    "Net Income": 95.0,
                    "Diluted EPS": 12.0,
                }
            }
        )
        mock_instance.balance_sheet = pd.DataFrame(
            {
                pd.Timestamp("2024-03-31"): {
                    "Total Assets": 1000.0,
                    "Current Liabilities": 200.0,
                    "Stockholders Equity": 450.0,
                    "Current Assets": 360.0,
                    "Cash And Cash Equivalents": 90.0,
                    "Total Debt": 150.0,
                    "Total Liabilities Net Minority Interest": 550.0,
                }
            }
        )
        mock_instance.cashflow = pd.DataFrame(
            {
                pd.Timestamp("2024-03-31"): {
                    "Operating Cash Flow": 140.0,
                    "Investing Cash Flow": -40.0,
                    "Financing Cash Flow": -20.0,
                    "Capital Expenditure": -30.0,
                }
            }
        )
        mock_ticker.return_value = mock_instance

        result = fetch_fundamentals("RELIANCE.NS")

        self.assertEqual(result["symbol"], "RELIANCE.NS")
        self.assertEqual(result["metrics"][0]["market_cap"], 1000000)
        self.assertEqual(result["metrics"][0]["pe"], 15.5)
        self.assertEqual(result["metrics"][0]["pat"], 95.0)
        self.assertGreater(result["metrics"][0]["roce"], 0)
        self.assertEqual(result["profit_loss"][0]["revenue"], 500.0)


if __name__ == "__main__":
    unittest.main()
