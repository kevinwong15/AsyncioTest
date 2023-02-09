import time
from sqlalchemy.sql import func
from session import Session
from models import AgeNext, Scenario

def get_scenarios():
    with Session() as session:
        scenarios = session.query(AgeNext, Scenario).join(Scenario).all()
        return (session, scenarios)

def update_scenarios(session, scenarios):

    for age_next, scenario in scenarios:
        age_next.is_success = False
        age_next.start_date = func.now()
        session.commit()

        # time.sleep(1)
        age_next.end_date = func.now()
        session.commit()

if __name__ == '__main__':
    # with Session() as session:
    #     scenarios = get_scenarios(session)
    #     update_scenarios(session, scenarios)

    session, scenarios = get_scenarios()
    update_scenarios(session, scenarios)