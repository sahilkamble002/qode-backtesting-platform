import pandas as pd

def sample_financial_metrics():
    return pd.DataFrame(
        [
            {"symbol": "AAA", "report_date": pd.Timestamp("2023-12-31"), "roe": 0.22, "pe": 12.0, "market_cap": 1_000_000.0, "roce": 0.18, "pat": 100.0, "debt_to_equity": 0.4, "current_ratio": 1.8},
            {"symbol": "BBB", "report_date": pd.Timestamp("2023-12-31"), "roe": 0.18, "pe": 18.0, "market_cap": 800_000.0, "roce": 0.15, "pat": 90.0, "debt_to_equity": 0.5, "current_ratio": 1.5},
            {"symbol": "CCC", "report_date": pd.Timestamp("2023-12-31"), "roe": 0.12, "pe": 25.0, "market_cap": 600_000.0, "roce": 0.11, "pat": 75.0, "debt_to_equity": 0.8, "current_ratio": 1.2},
            {"symbol": "DDD", "report_date": pd.Timestamp("2023-12-31"), "roe": 0.27, "pe": 10.0, "market_cap": 1_200_000.0, "roce": 0.2, "pat": 110.0, "debt_to_equity": 0.3, "current_ratio": 2.0},
        ]
    )

def historical_financial_metrics():
    return pd.DataFrame(
        [
            {"symbol": "AAA", "report_date": pd.Timestamp("2023-12-31"), "roe": 0.22, "pe": 12.0, "market_cap": 1_000_000.0, "roce": 0.18, "pat": 100.0, "debt_to_equity": 0.4, "current_ratio": 1.8},
            {"symbol": "AAA", "report_date": pd.Timestamp("2024-01-31"), "roe": 0.10, "pe": 30.0, "market_cap": 1_050_000.0, "roce": 0.08, "pat": 60.0, "debt_to_equity": 0.6, "current_ratio": 1.1},
            {"symbol": "BBB", "report_date": pd.Timestamp("2023-12-31"), "roe": 0.16, "pe": 14.0, "market_cap": 900_000.0, "roce": 0.14, "pat": 88.0, "debt_to_equity": 0.5, "current_ratio": 1.6},
            {"symbol": "BBB", "report_date": pd.Timestamp("2024-01-31"), "roe": 0.31, "pe": 11.0, "market_cap": 950_000.0, "roce": 0.24, "pat": 140.0, "debt_to_equity": 0.35, "current_ratio": 1.9},
            {"symbol": "DDD", "report_date": pd.Timestamp("2023-12-31"), "roe": 0.27, "pe": 10.0, "market_cap": 1_200_000.0, "roce": 0.20, "pat": 110.0, "debt_to_equity": 0.3, "current_ratio": 2.0},
            {"symbol": "DDD", "report_date": pd.Timestamp("2024-01-31"), "roe": 0.26, "pe": 10.5, "market_cap": 1_180_000.0, "roce": 0.19, "pat": 108.0, "debt_to_equity": 0.31, "current_ratio": 1.95},
        ]
    )

def sample_price_data():
    return pd.DataFrame(
        [
            {"symbol": "AAA", "date": pd.Timestamp("2024-01-01"), "open": 100.0, "high": 102.0, "low": 99.0, "close": 100.0, "volume": 1000.0},
            {"symbol": "AAA", "date": pd.Timestamp("2024-01-31"), "open": 104.0, "high": 106.0, "low": 103.0, "close": 105.0, "volume": 1200.0},
            {"symbol": "BBB", "date": pd.Timestamp("2024-01-01"), "open": 200.0, "high": 202.0, "low": 198.0, "close": 200.0, "volume": 1100.0},
            {"symbol": "BBB", "date": pd.Timestamp("2024-01-31"), "open": 209.0, "high": 211.0, "low": 208.0, "close": 210.0, "volume": 1300.0},
            {"symbol": "AAA", "date": pd.Timestamp("2024-02-01"), "open": 106.0, "high": 108.0, "low": 105.0, "close": 106.0, "volume": 1150.0},
            {"symbol": "AAA", "date": pd.Timestamp("2024-02-29"), "open": 111.0, "high": 113.0, "low": 110.0, "close": 112.0, "volume": 1250.0},
            {"symbol": "BBB", "date": pd.Timestamp("2024-02-01"), "open": 208.0, "high": 210.0, "low": 207.0, "close": 208.0, "volume": 1180.0},
            {"symbol": "BBB", "date": pd.Timestamp("2024-02-29"), "open": 214.0, "high": 216.0, "low": 213.0, "close": 215.0, "volume": 1280.0},
            {"symbol": "DDD", "date": pd.Timestamp("2024-01-01"), "open": 50.0, "high": 51.0, "low": 49.0, "close": 50.0, "volume": 900.0},
            {"symbol": "DDD", "date": pd.Timestamp("2024-01-31"), "open": 55.0, "high": 56.0, "low": 54.0, "close": 55.0, "volume": 1000.0},
            {"symbol": "DDD", "date": pd.Timestamp("2024-02-01"), "open": 56.0, "high": 57.0, "low": 55.0, "close": 56.0, "volume": 980.0},
            {"symbol": "DDD", "date": pd.Timestamp("2024-02-29"), "open": 58.0, "high": 60.0, "low": 57.0, "close": 59.0, "volume": 1100.0},
        ]
    )
