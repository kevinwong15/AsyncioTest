import aiohttp
import asyncio

from db.models import AgeNext, Scenario
from db.session import Session
from sqlalchemy.sql import func

from typing import Tuple

def load_download_data():
    with Session() as session:
        scenarios = session.query(AgeNext, Scenario).join(Scenario).all()
        return scenarios

async def get_page(session, sem, id, url: Tuple[AgeNext, Scenario], viewer):

    age_next, scenario = url

    with Session() as db_session:
        age_next.start_date = func.now()
        db_session.commit()

    async with sem:
        viewer.update_status(id, f'Downloading {id}...')


        with Session() as db_session:
            age_next.start_date = func.now()
            db_session.commit()

        await download_page(session, id, scenario.url, age_next.age)

        with Session() as db_session:
            age_next.is_success = True
            age_next.end_date = func.now()
            db_session.commit()

async def download_page(session, id, url, age):

        async with session.get(url) as r:

            result = await r.text()
            with open(f'data/test{id+1}-{age}.txt', 'w') as f:
                f.write(result)
            return result

async def download_all(viewer, connect_count):

    sem = asyncio.Semaphore(connect_count)

    urls = load_download_data()

    async with aiohttp.ClientSession() as session:
        tasks = []
        for id, url in enumerate(urls):
            task = asyncio.create_task(get_page(session, sem, id, url, viewer))
            tasks.append(task)
        results = await asyncio.gather(*tasks)
        return results