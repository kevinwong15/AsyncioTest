
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Float
from sqlalchemy.sql import func
from db.orm_base import Base


class AgeNext(Base):
    __tablename__ = "age"
    id = Column(Integer, primary_key=True)
    age = Column(Integer)
    is_downloaded = Column(Boolean, default=False)
    is_processed = Column(Boolean, default=False)
    scenario_id = Column(Integer, ForeignKey("scenario.id"))
    download_time = Column(Float)
    download_at = Column(DateTime(timezone=True))
    processed_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    modified_at = Column(DateTime(timezone=True), onupdate=func.now())


class Scenario(Base):
    __tablename__ = 'scenario'
    id = Column(Integer, primary_key=True)
    url = Column(String)
    ages = relationship("AgeNext")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    modified_at = Column(DateTime(timezone=True), onupdate=func.now())
