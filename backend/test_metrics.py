import unittest
from unittest.mock import patch
from app.services.backtest_engine import run_backtest
from app.services.metrics_engine import build_backtest_insights, calculate_metrics
from testing_data import sample_financial_metrics, sample_price_data
class MetricsEngineTests(unittest.TestCase):
    @patch("app.services.backtest_engine.select_stocks")
    def test_calculates_summary_metrics(self, mock_select_stocks):
        mock_select_stocks.side_effect = [
            sample_financial_metrics().iloc[[0, 3]].reset_index(drop=True),
            sample_financial_metrics().iloc[[1, 3]].reset_index(drop=True),
        ]

        portfolio = run_backtest(
            data=sample_price_data(),
            start_date="2024-01-01",
            end_date="2024-02-29",
            initial_capital=100000,
        )

        result = calculate_metrics(portfolio)

        self.assertEqual(result["number_of_rebalances"], 2)
        self.assertGreater(result["final_capital"], result["initial_capital"])
        self.assertIn("sharpe_ratio", result)
        insights = build_backtest_insights(portfolio)
        self.assertEqual(len(insights["equity_curve"]), 2)
        self.assertTrue(insights["top_winners"])

    def test_empty_portfolio_metrics(self):
        result = calculate_metrics(sample_price_data().iloc[0:0])

        self.assertEqual(result["portfolio_entries"], 0)
        self.assertEqual(result["final_capital"], 0.0)

if __name__ == "__main__":
    unittest.main()
