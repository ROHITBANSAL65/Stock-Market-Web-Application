import yfinance as yf
from app.db import engine, SessionLocal
from app.models import Base, Company, HistoricalPrice

# Create tables if not exist
Base.metadata.create_all(bind=engine)

session = SessionLocal()

# Clear existing data
session.query(HistoricalPrice).delete()
session.query(Company).delete()
session.commit()

companies = [
    {"symbol": "AAPL", "name": "Apple Inc."},
    {"symbol": "MSFT", "name": "Microsoft Corporation"},
    {"symbol": "GOOGL", "name": "Alphabet Inc."},
    {"symbol": "AMZN", "name": "Amazon.com, Inc."},
    {"symbol": "TSLA", "name": "Tesla, Inc."},
    {"symbol": "META", "name": "Meta Platforms, Inc."},
    {"symbol": "NFLX", "name": "Netflix, Inc."},
    {"symbol": "NVDA", "name": "NVIDIA Corporation"},
    {"symbol": "INTC", "name": "Intel Corporation"},
    {"symbol": "IBM", "name": "International Business Machines Corporation"},
]

# Add companies
for comp in companies:
    company = Company(symbol=comp["symbol"], name=comp["name"])
    session.add(company)
session.commit()

# Download and insert historical prices
for comp in companies:
    data = yf.download(comp["symbol"], period="1mo", interval="1d", auto_adjust=False)
    for date, row in data.iterrows():
        price = HistoricalPrice(
            symbol=comp["symbol"],
            date=date.date(),
            open=float(row["Open"]),
            high=float(row["High"]),
            low=float(row["Low"]),
            close=float(row["Close"]),
            volume=int(row["Volume"])
        )
        session.add(price)

session.commit()
session.close()
print("Database seeded successfully.")
