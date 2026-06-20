import unittest
from unittest.mock import patch
from app.services.backtest_engine import run_backtest
from testing_data import sample_financial_metrics, sample_price_data
class BacktestEngineTests(unittest.TestCase):
    @patch("app.services.backtest_engine.select_stocks")
    def test_backtest_generates_period_returns_and_capital_progression(self, mock_select_stocks):
        mock_select_stocks.side_effect = [
            sample_financial_metrics().iloc[[0, 3]].reset_index(drop=True),
            sample_financial_metrics().iloc[[1, 3]].reset_index(drop=True),
        ]

        result = run_backtest(
            data=sample_price_data(),
            start_date="2024-01-01",
            end_date="2024-02-29",
            initial_capital=100000,
            rebalance_frequency="monthly",
            portfolio_size=2,
        )

        self.assertFalse(result.empty)
        self.assertIn("capital_end", result.columns)
        self.assertIn("return_pct", result.columns)
        self.assertGreater(result["capital_end"].iloc[-1], result["capital_start"].iloc[0])
        self.assertEqual(mock_select_stocks.call_count, 2)
        self.assertIn("BBB", result[result["rebalance_date"] == "2024-02-01"]["symbol"].tolist())

    @patch("app.services.backtest_engine.select_stocks")
    def test_returns_empty_when_strategy_has_no_matches(self, mock_select_stocks):
        mock_select_stocks.return_value = sample_financial_metrics().iloc[0:0]

        result = run_backtest(
            data=sample_price_data(),
            start_date="2024-01-01",
            end_date="2024-02-29",
            initial_capital=100000,
        )

        self.assertTrue(result.empty)


if __name__ == "__main__":
    unittest.main()
