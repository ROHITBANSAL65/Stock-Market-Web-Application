# from fastapi import FastAPI, Depends, HTTPException
# from sqlalchemy.orm import Session
# from typing import List, Optional
# from datetime import date, datetime, timedelta
# from .db import SessionLocal, engine
# from .models import Base, Company as CompanyModel, HistoricalPrice as HPModel
# from . import schemas
# from fastapi.middleware.cors import CORSMiddleware

# Base.metadata.create_all(bind=engine)
# app = FastAPI()

# origins = [
#     "http://localhost:3000",
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# @app.get('/companies', response_model=List[schemas.Company])
# def get_companies(db: Session = Depends(get_db)):
#     return db.query(CompanyModel).all()

# @app.get('/historical/{symbol}', response_model=List[schemas.HistoricalPrice])
# def get_historical(
#     symbol: str, 
#     start: Optional[str] = None, 
#     end: Optional[str] = None, 
#     db: Session = Depends(get_db)
# ):
#     q = db.query(HPModel).filter(HPModel.symbol == symbol)
#     if start:
#         q = q.filter(HPModel.date >= start)
#     if end:
#         q = q.filter(HPModel.date <= end)
#     rows = q.order_by(HPModel.date).all()
#     if not rows:
#         raise HTTPException(status_code=404, detail='No data')
#     return rows

# @app.get('/stats/{symbol}', response_model=schemas.Stats)
# def stats(symbol: str, db: Session = Depends(get_db)):
#     one_year_ago = datetime.now() - timedelta(days=365)
#     rows = db.query(HPModel).filter(
#         HPModel.symbol == symbol,
#         HPModel.date >= one_year_ago.date()
#     ).all()

#     if not rows:
#         raise HTTPException(status_code=404, detail='No data')

#     closes = [r.close for r in rows if r.close is not None]
#     vols = [r.volume for r in rows if r.volume is not None]

#     return schemas.Stats(
#         week_52_high=max(closes) if closes else None,
#         week_52_low=min(closes) if closes else None,
#         avg_volume=sum(vols) / len(vols) if vols else None
#     )


from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, datetime, timedelta
from .db import SessionLocal, engine
from .models import Base, Company as CompanyModel, HistoricalPrice as HPModel
from . import schemas
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)
app = FastAPI()

# Allow requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # <-- changed here
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/companies', response_model=List[schemas.Company])
def get_companies(db: Session = Depends(get_db)):
    return db.query(CompanyModel).all()

@app.get('/historical/{symbol}', response_model=List[schemas.HistoricalPrice])
def get_historical(
    symbol: str, 
    start: Optional[str] = None, 
    end: Optional[str] = None, 
    db: Session = Depends(get_db)
):
    q = db.query(HPModel).filter(HPModel.symbol == symbol)
    if start:
        q = q.filter(HPModel.date >= start)
    if end:
        q = q.filter(HPModel.date <= end)
    rows = q.order_by(HPModel.date).all()
    if not rows:
        raise HTTPException(status_code=404, detail='No data')
    return rows

@app.get('/stats/{symbol}', response_model=schemas.Stats)
def stats(symbol: str, db: Session = Depends(get_db)):
    one_year_ago = datetime.now() - timedelta(days=365)
    rows = db.query(HPModel).filter(
        HPModel.symbol == symbol,
        HPModel.date >= one_year_ago.date()
    ).all()

    if not rows:
        raise HTTPException(status_code=404, detail='No data')

    closes = [r.close for r in rows if r.close is not None]
    vols = [r.volume for r in rows if r.volume is not None]

    return schemas.Stats(
        week_52_high=max(closes) if closes else None,
        week_52_low=min(closes) if closes else None,
        avg_volume=sum(vols) / len(vols) if vols else None
    )


