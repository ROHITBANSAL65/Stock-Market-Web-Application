from sqlalchemy import Column, Integer, String, Float, Date
from app.db import Base

class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, index=True)
    name = Column(String)

class HistoricalPrice(Base):
    __tablename__ = "historical_prices"
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    date = Column(Date, index=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Float)
