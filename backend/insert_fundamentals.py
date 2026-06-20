from app.database import SessionLocal
from app.models.financial_metric import FinancialMetric
from app.models.financial_statements import (
    BalanceSheetStatement,
    CashFlowStatement,
    ProfitLossStatement,
)
from app.services.data_fetcher import STOCKS
from app.services.fundamental_fetcher import fetch_fundamentals

db = SessionLocal()

for symbol in STOCKS:
    try:
        print(f"Fetching {symbol}")
        data = fetch_fundamentals(symbol)

        existing_metric_dates = {
            row[0]
            for row in db.query(FinancialMetric.report_date).filter(
                FinancialMetric.symbol == symbol
            ).all()
        }

        for metric_data in data["metrics"]:
            if metric_data["report_date"] in existing_metric_dates:
                continue
            db.add(FinancialMetric(**metric_data))

        for statement_key, model in (
            ("profit_loss", ProfitLossStatement),
            ("balance_sheet", BalanceSheetStatement),
            ("cash_flow", CashFlowStatement),
        ):
            existing_statement_dates = {
                row[0]
                for row in db.query(model.report_date).filter(
                    model.symbol == symbol
                ).all()
            }

            for statement_row in data[statement_key]:
                if statement_row["report_date"] in existing_statement_dates:
                    continue
                db.add(model(**statement_row))

    except Exception as e:
        print(f"Failed: {symbol}")
        print(e)
        continue

db.commit()
db.close()
print("Fundamental data inserted successfully")
