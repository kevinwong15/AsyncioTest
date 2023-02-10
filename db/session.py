from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sqlite_path = r'progress.sqlite3'
engine = create_engine(f'sqlite:///{sqlite_path}', echo=False)
Session = sessionmaker(bind=engine)