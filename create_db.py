from sqlalchemy.sql import func
from db.session import Session
from db.models import AgeNext, Scenario
from sqlalchemy import create_engine

from db.orm_base import Base

def create_db():
    sqlite_path = r'c:\temp\repo\test_bed\progress.db'
    engine = create_engine(f'sqlite:///{sqlite_path}', echo=True)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def create_scenarios():
    # create session and add objects
    with Session() as session:
        items = [
            Scenario(
                url=f'https://books.toscrape.com/catalogue/page-{id+1}.html',
                ages=[AgeNext(age=i) for i in range(0, 10)]
            )
            for id in range(0, 50)
        ]
        session.add_all(items)
        session.commit()


if __name__ == '__main__':
    create_db()
    create_scenarios()
