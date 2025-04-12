from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel

DATABASE_URL = "postgresql://neondb_owner:npg_QG8KrAXgzp3f@ep-holy-hill-a2798f83-pooler.eu-central-1.aws.neon.tech/neondb?sslmode=require"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define the database model
class Report(Base):
    __tablename__ = "reports"
    id = Column(Integer, primary_key=True, index=True)
    shop_name = Column(String, index=True)
    rating = Column(Integer)
    feedback = Column(String)

Base.metadata.create_all(bind=engine)

# Define Pydantic model for API response
class ReportResponse(BaseModel):
    shop_name: str
    rating: int
    feedback: str

app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API to submit a new report
@app.post("/report")
def create_report(shop_name: str, rating: int, feedback: str, db: Session = Depends(get_db)):
    new_report = Report(shop_name=shop_name, rating=rating, feedback=feedback)
    db.add(new_report)
    db.commit()
    return {"message": "Report submitted!"}

# API to retrieve all reports
@app.get("/reports", response_model=list[ReportResponse])
def get_reports(db: Session = Depends(get_db)):
    reports = db.query(Report).all()
    return [ReportResponse(shop_name=r.shop_name, rating=r.rating, feedback=r.feedback) for r in reports]
