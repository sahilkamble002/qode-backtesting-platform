from app.database import SessionLocal
from app.models.models import StockPrice
from app.services.data_fetcher import fetch_stock_data
db = SessionLocal()
data = fetch_stock_data()
data.columns = [col.lower() for col in data.columns]
data.rename(columns={"date": "date"}, inplace=True)
data["date"] = data["date"].dt.date

for _, row in data.iterrows():

    stock = StockPrice(
        symbol=row["symbol"],
        date=row["date"],
        open=float(row["open"]),
        high=float(row["high"]),
        low=float(row["low"]),
        close=float(row["close"]),
        volume=float(row["volume"])
    )

    db.add(stock)

db.commit()
db.close()
print("Data inserted successfully")