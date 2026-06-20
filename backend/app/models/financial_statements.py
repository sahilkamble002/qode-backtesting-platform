from sqlalchemy import Column, Date, Float, Integer, String

from app.models.models import Base


class ProfitLossStatement(Base):
    __tablename__ = "profit_loss_statements"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    report_date = Column(Date, index=True)
    revenue = Column(Float)
    ebit = Column(Float)
    pretax_income = Column(Float)
    net_income = Column(Float)
    eps = Column(Float)
    last_updated = Column(Date)


class BalanceSheetStatement(Base):
    __tablename__ = "balance_sheet_statements"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    report_date = Column(Date, index=True)
    total_assets = Column(Float)
    total_liabilities = Column(Float)
    total_equity = Column(Float)
    current_assets = Column(Float)
    current_liabilities = Column(Float)
    cash_and_equivalents = Column(Float)
    total_debt = Column(Float)
    capital_employed = Column(Float)
    last_updated = Column(Date)


class CashFlowStatement(Base):
    __tablename__ = "cash_flow_statements"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    report_date = Column(Date, index=True)
    operating_cash_flow = Column(Float)
    investing_cash_flow = Column(Float)
    financing_cash_flow = Column(Float)
    capital_expenditure = Column(Float)
    free_cash_flow = Column(Float)
    last_updated = Column(Date)
