import unittest
from unittest.mock import MagicMock, patch

from app.services.load_data import load_stock_data
from testing_data import sample_price_data


class LoadDataTests(unittest.TestCase):
    @patch("app.services.load_data.pd.read_sql")
    @patch("app.services.load_data.engine")
    def test_load_stock_data_returns_dataframe(self, mock_engine, mock_read_sql):
        connection = MagicMock()
        mock_engine.connect.return_value.__enter__.return_value = connection
        mock_read_sql.return_value = sample_price_data()

        result = load_stock_data()

        self.assertFalse(result.empty)
        self.assertIn("date", result.columns)


if __name__ == "__main__":
    unittest.main()
