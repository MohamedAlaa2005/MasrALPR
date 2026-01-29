from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

SQLALCHEMY_DATABASE_URL = "sqlite:///./plates_intel.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class PlateRecord(Base):
    __tablename__ = "plate_records"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    is_allowed = Column(Boolean, default=True)
    image_name = Column(String)

class BlacklistedPlate(Base):
    __tablename__ = "blacklist"
    id = Column(Integer, primary_key=True, index=True)
    plate_text = Column(String, unique=True) # Can be a full plate or just a letter

Base.metadata.create_all(bind=engine)