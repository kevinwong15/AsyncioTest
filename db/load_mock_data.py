
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy.sql import func
from session import Session

from models import AgeNext, Scenario

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
    create_scenarios()
