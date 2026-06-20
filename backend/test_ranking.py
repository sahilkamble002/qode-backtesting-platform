import unittest

from app.services.ranking_engine import rank_stocks
from testing_data import sample_financial_metrics


class RankingEngineTests(unittest.TestCase):
    def test_ranks_descending(self):
        data = sample_financial_metrics()

        result = rank_stocks(data, metric="roe", ascending=False)

        self.assertEqual(result.iloc[0]["symbol"], "DDD")
        self.assertEqual(result.iloc[-1]["symbol"], "CCC")

    def test_raises_for_missing_metric(self):
        data = sample_financial_metrics()

        with self.assertRaises(ValueError):
            rank_stocks(data, metric="unknown_metric")

    def test_ranks_using_composite_metrics(self):
        data = sample_financial_metrics()

        result = rank_stocks(data, metrics=["roe", "roce"], ascending=False)

        self.assertEqual(result.iloc[0]["symbol"], "DDD")
        self.assertIn("composite_rank", result.columns)


if __name__ == "__main__":
    unittest.main()
