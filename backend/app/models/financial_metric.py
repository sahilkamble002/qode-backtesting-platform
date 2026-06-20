
from sqlalchemy import Column, Date, Float, Integer, String

from app.models.models import Base


class FinancialMetric(Base):

    __tablename__ = "financial_metrics"

    id = Column(Integer, primary_key=True, index=True)

    symbol = Column(String, index=True)
    report_date = Column(Date, index=True)

    market_cap = Column(Float)

    pe = Column(Float)

    roe = Column(Float)

    roce = Column(Float)

    pat = Column(Float)

    debt_to_equity = Column(Float)

    current_ratio = Column(Float)

    last_updated = Column(Date)
