import unittest
from unittest.mock import patch
from pydantic import ValidationError
from app.main import _run_backtest
from app.schemas.backtest import BacktestRequest
from testing_data import sample_financial_metrics, sample_price_data
class BacktestApiTests(unittest.TestCase):
    @patch("app.main.load_stock_data")
    @patch("app.services.backtest_engine.select_stocks")
    def test_run_backtest_response_contains_records_and_metrics(self, mock_select_stocks, mock_load_stock_data):
        mock_load_stock_data.return_value = sample_price_data()
        mock_select_stocks.side_effect = [
            sample_financial_metrics().iloc[[0, 3]].reset_index(drop=True),
            sample_financial_metrics().iloc[[1, 3]].reset_index(drop=True),
        ]

        response = _run_backtest(
            BacktestRequest(
                start_date="2024-01-01",
                end_date="2024-02-29",
                initial_capital=100000,
                portfolio_size=2,
            )
        )

        self.assertGreater(response.total_records, 0)
        self.assertGreater(response.metrics.final_capital, response.metrics.initial_capital)
        self.assertEqual(len(response.equity_curve), 2)
        self.assertTrue(response.top_winners)

    def test_backtest_request_rejects_invalid_dates(self):
        with self.assertRaises(ValidationError):
            BacktestRequest(
                start_date="2024-03-01",
                end_date="2024-02-01",
                initial_capital=100000,
                portfolio_size=2,
            )


if __name__ == "__main__":
    unittest.main()
