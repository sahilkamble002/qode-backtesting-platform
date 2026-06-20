import unittest
from unittest.mock import patch
from app.services.strategy_engine import select_stocks
from testing_data import historical_financial_metrics, sample_financial_metrics
class StrategyEngineTests(unittest.TestCase):
    @patch("app.services.strategy_engine.load_financial_metrics")
    def test_selects_filtered_and_ranked_stocks(self, mock_load_financial_metrics):
        mock_load_financial_metrics.return_value = sample_financial_metrics()

        result = select_stocks(
            portfolio_size=2,
            min_roe=0.15,
            max_pe=20,
            ranking_metric="roe",
            ranking_ascending=False,
        )

        self.assertEqual(result["symbol"].tolist(), ["DDD", "AAA"])

    @patch("app.services.strategy_engine.load_financial_metrics")
    def test_limits_to_universe_symbols(self, mock_load_financial_metrics):
        mock_load_financial_metrics.return_value = sample_financial_metrics()

        result = select_stocks(
            portfolio_size=3,
            universe_symbols=["AAA", "BBB"],
        )

        self.assertTrue(set(result["symbol"]).issubset({"AAA", "BBB"}))

    @patch("app.services.strategy_engine.load_financial_metrics")
    def test_uses_historical_snapshot_without_future_leakage(self, mock_load_financial_metrics):
        history = historical_financial_metrics()

        def fake_load_financial_metrics(as_of_date=None):
            filtered = history[history["report_date"] <= as_of_date].copy()
            filtered = filtered.sort_values(["symbol", "report_date"])
            return filtered.groupby("symbol", as_index=False).tail(1).reset_index(drop=True)

        mock_load_financial_metrics.side_effect = fake_load_financial_metrics

        result = select_stocks(
            portfolio_size=2,
            ranking_metric="roe",
            rebalance_date="2024-01-01",
        )

        mock_load_financial_metrics.assert_called_once_with(as_of_date="2024-01-01")
        self.assertEqual(result["symbol"].tolist(), ["DDD", "AAA"])


if __name__ == "__main__":
    unittest.main()
