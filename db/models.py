from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy import create_engine

Base = declarative_base()

class AgeNext(Base):
    __tablename__ = "age"
    id = Column(Integer, primary_key=True)
    age = Column(Integer)
    is_success = Column(Boolean, default=False)
    scenario_id = Column(Integer, ForeignKey("scenario.id"))
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    modified_at = Column(DateTime(timezone=True), onupdate=func.now())

class Scenario(Base):
    __tablename__ = 'scenario'
    id = Column(Integer, primary_key=True)
    url = Column(String)
    ages = relationship("AgeNext")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    modified_at = Column(DateTime(timezone=True), onupdate=func.now())

def create_db():
    sqlite_path = r'c:\temp\repo\test_bed\progress.db'
    engine = create_engine(f'sqlite:///{sqlite_path}', echo=True)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    create_db()
