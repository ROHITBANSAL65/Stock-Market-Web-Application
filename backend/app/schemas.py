from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date

class Company(BaseModel):
    id: int
    symbol: str
    name: Optional[str] = None

    class Config:
        from_attributes = True

class HistoricalPrice(BaseModel):
    id: int
    symbol: str
    date: date
    open: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    close: Optional[float] = None
    volume: Optional[float] = None

    class Config:
        from_attributes = True

class StockData(BaseModel):
    symbol: str
    name: Optional[str] = None
    price: Optional[float] = None
    change: Optional[float] = None
    percent_change: Optional[float] = None

    class Config:
        from_attributes = True
        validate_by_name = True

class Stats(BaseModel):
    week_52_high: Optional[float] = Field(None, alias="52_week_high")
    week_52_low: Optional[float] = Field(None, alias="52_week_low")
    avg_volume: Optional[float] = None
    market_cap: Optional[float] = None
    pe_ratio: Optional[float] = None

    class Config:
        from_attributes = True
        validate_by_name = True

class StockDetails(BaseModel):
    symbol: str
    name: Optional[str] = None
    price: Optional[float] = None
    change: Optional[float] = None
    percent_change: Optional[float] = None
    stats: Optional[Stats] = None
    history: Optional[List[float]] = None

    class Config:
        from_attributes = True
        validate_by_name = True
