
import aiohttp
import asyncio
import time
from db.models import AgeNext, Scenario
from db.session import Session
from sqlalchemy.sql import func
from typing import Tuple
from viewer import StatusViewer


def load_download_data(db_session):
    scenarios = (
        db_session
        .query(AgeNext, Scenario)
        .join(Scenario)
        .filter(AgeNext.is_downloaded == False)
        .all()
    )
    return scenarios


async def get_page(db_session, session, sem, id,
                   url: Tuple[AgeNext, Scenario],
                   viewer: StatusViewer):

    age_next, scenario = url
    async with sem:

        node_id = viewer.start_node(f'Downloading {id}...')
        start_time = time.time()

        age_next.download_at = func.now()
        db_session.commit()

        try:
            await download_page(session, id, scenario.url, age_next.age)
            age_next.is_downloaded = True
            age_next.download_time = time.time() - start_time
            db_session.commit()
        except:
            pass

        viewer.completed_count += 1
        viewer.release_node(node_id, '')


async def download_page(session, id, url, age):
    async with session.get(url) as r:
        result = await r.text()
        with open(f'data/test{id+1}-{age}.txt', 'w') as f:
            f.write(result)
        return result


async def download_all(viewer: StatusViewer, connect_count):

    sem = asyncio.Semaphore(connect_count)

    with Session() as db_session:

        urls = load_download_data(db_session)
        viewer.total_count = len(urls)

        async with aiohttp.ClientSession() as session:
            tasks = []
            for id, url in enumerate(urls):
                task = asyncio.create_task(
                    get_page(db_session, session, sem, id, url, viewer))
                tasks.append(task)
            results = await asyncio.gather(*tasks)
            return results
