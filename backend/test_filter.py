import unittest
from app.services.filter_engine import filter_stocks
from testing_data import sample_financial_metrics
class FilterEngineTests(unittest.TestCase):
    def test_filters_by_roe_and_pe(self):
        data = sample_financial_metrics()

        result = filter_stocks(
            data=data,
            min_roe=0.18,
            max_pe=15,
        )

        self.assertEqual(result["symbol"].tolist(), ["AAA", "DDD"])

    def test_filters_by_market_cap(self):
        data = sample_financial_metrics()

        result = filter_stocks(
            data=data,
            min_market_cap=1_000_000,
        )

        self.assertEqual(result["symbol"].tolist(), ["AAA", "DDD"])

    def test_filters_by_market_cap_range(self):
        data = sample_financial_metrics()

        result = filter_stocks(
            data=data,
            min_market_cap=700_000,
            max_market_cap=1_000_000,
        )

        self.assertEqual(result["symbol"].tolist(), ["AAA", "BBB"])

if __name__ == "__main__":
    unittest.main()
