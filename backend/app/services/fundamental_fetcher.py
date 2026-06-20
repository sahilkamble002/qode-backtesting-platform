from datetime import date

import pandas as pd
import yfinance as yf


def _safe_value(frame, label, column):
    if frame is None or frame.empty or label not in frame.index or column not in frame.columns:
        return None

    value = frame.at[label, column]
    if pd.isna(value):
        return None

    return float(value)


def _statement_columns(*frames):
    columns = set()
    for frame in frames:
        if frame is not None and not frame.empty:
            columns.update(frame.columns.tolist())
    return sorted(columns)


def _to_report_date(value):
    return pd.to_datetime(value).date()


def _compute_capital_employed(balance_sheet, column):
    total_assets = _safe_value(balance_sheet, "Total Assets", column)
    current_liabilities = _safe_value(balance_sheet, "Current Liabilities", column)
    total_equity = _safe_value(balance_sheet, "Stockholders Equity", column)
    total_debt = _safe_value(balance_sheet, "Total Debt", column)

    if total_assets is not None and current_liabilities is not None:
        return total_assets - current_liabilities

    if total_equity is not None or total_debt is not None:
        return (total_equity or 0.0) + (total_debt or 0.0)

    return None


def fetch_fundamentals(symbol):
    stock = yf.Ticker(symbol)
    info = stock.info
    income_statement = stock.income_stmt
    balance_sheet = stock.balance_sheet
    cash_flow = stock.cashflow

    report_dates = _statement_columns(income_statement, balance_sheet, cash_flow)
    snapshots = []
    profit_loss_rows = []
    balance_sheet_rows = []
    cash_flow_rows = []

    for column in report_dates:
        report_date = _to_report_date(column)
        revenue = _safe_value(income_statement, "Total Revenue", column)
        ebit = _safe_value(income_statement, "EBIT", column)
        pretax_income = _safe_value(income_statement, "Pretax Income", column)
        net_income = _safe_value(income_statement, "Net Income", column)
        eps = _safe_value(income_statement, "Diluted EPS", column)
        total_assets = _safe_value(balance_sheet, "Total Assets", column)
        total_liabilities = _safe_value(
            balance_sheet, "Total Liabilities Net Minority Interest", column
        )
        total_equity = _safe_value(balance_sheet, "Stockholders Equity", column)
        current_assets = _safe_value(balance_sheet, "Current Assets", column)
        current_liabilities = _safe_value(balance_sheet, "Current Liabilities", column)
        cash_and_equivalents = _safe_value(
            balance_sheet, "Cash And Cash Equivalents", column
        )
        total_debt = _safe_value(balance_sheet, "Total Debt", column)
        capital_employed = _compute_capital_employed(balance_sheet, column)
        operating_cash_flow = _safe_value(cash_flow, "Operating Cash Flow", column)
        investing_cash_flow = _safe_value(cash_flow, "Investing Cash Flow", column)
        financing_cash_flow = _safe_value(cash_flow, "Financing Cash Flow", column)
        capital_expenditure = _safe_value(cash_flow, "Capital Expenditure", column)
        free_cash_flow = None
        if operating_cash_flow is not None and capital_expenditure is not None:
            free_cash_flow = operating_cash_flow + capital_expenditure

        profit_loss_rows.append(
            {
                "symbol": symbol,
                "report_date": report_date,
                "revenue": revenue,
                "ebit": ebit,
                "pretax_income": pretax_income,
                "net_income": net_income,
                "eps": eps,
                "last_updated": date.today(),
            }
        )

        balance_sheet_rows.append(
            {
                "symbol": symbol,
                "report_date": report_date,
                "total_assets": total_assets,
                "total_liabilities": total_liabilities,
                "total_equity": total_equity,
                "current_assets": current_assets,
                "current_liabilities": current_liabilities,
                "cash_and_equivalents": cash_and_equivalents,
                "total_debt": total_debt,
                "capital_employed": capital_employed,
                "last_updated": date.today(),
            }
        )

        cash_flow_rows.append(
            {
                "symbol": symbol,
                "report_date": report_date,
                "operating_cash_flow": operating_cash_flow,
                "investing_cash_flow": investing_cash_flow,
                "financing_cash_flow": financing_cash_flow,
                "capital_expenditure": capital_expenditure,
                "free_cash_flow": free_cash_flow,
                "last_updated": date.today(),
            }
        )

        current_ratio = None
        if current_assets is not None and current_liabilities not in (None, 0):
            current_ratio = current_assets / current_liabilities

        roe = None
        if net_income is not None and total_equity not in (None, 0):
            roe = net_income / total_equity
        elif info.get("returnOnEquity") is not None:
            roe = info.get("returnOnEquity")

        roce = None
        if ebit is not None and capital_employed not in (None, 0):
            roce = ebit / capital_employed

        snapshots.append(
            {
                "symbol": symbol,
                "report_date": report_date,
                "market_cap": info.get("marketCap"),
                "pe": info.get("trailingPE"),
                "roe": roe,
                "debt_to_equity": info.get("debtToEquity"),
                "current_ratio": current_ratio if current_ratio is not None else info.get("currentRatio"),
                "pat": net_income,
                "roce": roce,
                "last_updated": date.today(),
            }
        )

    if not snapshots:
        snapshots.append(
            {
                "symbol": symbol,
                "report_date": date.today(),
                "market_cap": info.get("marketCap"),
                "pe": info.get("trailingPE"),
                "roe": info.get("returnOnEquity"),
                "debt_to_equity": info.get("debtToEquity"),
                "current_ratio": info.get("currentRatio"),
                "pat": None,
                "roce": None,
                "last_updated": date.today(),
            }
        )

    return {
        "symbol": symbol,
        "metrics": snapshots,
        "profit_loss": profit_loss_rows,
        "balance_sheet": balance_sheet_rows,
        "cash_flow": cash_flow_rows,
    }
