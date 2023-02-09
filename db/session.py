from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sqlite_path = r'c:\temp\repo\test_bed\progress.db'
engine = create_engine(f'sqlite:///{sqlite_path}', echo=True)
Session = sessionmaker(bind=engine)