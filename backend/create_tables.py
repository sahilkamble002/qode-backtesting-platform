
from app.database import engine
from app.models.models import Base
from app.models.financial_metric import FinancialMetric
from app.models.financial_statements import (
    BalanceSheetStatement,
    CashFlowStatement,
    ProfitLossStatement,
)

Base.metadata.create_all(bind=engine)

print("Tables created successfully")


