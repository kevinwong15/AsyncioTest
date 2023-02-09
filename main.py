import asyncio

from download import download_all
from viewer import StatusViewer

from random import randint

async def main():

    connect_count = 1

    status_viewer = StatusViewer(connect_count)
    asyncio.create_task(status_viewer.start_timer())

    results = await download_all(status_viewer, connect_count)

    status_viewer.stop_timer()

async def main2():

    connect_count = 4
    status_viewer = StatusViewer(connect_count)
    asyncio.create_task(status_viewer.start_timer())

    ids = [i for i in range(0, 10)]
    for id in ids:
        wait_time = randint(1, 3)
        await asyncio.sleep(wait_time)

        status_viewer.update_status(id, f'Ran {id}')

    status_viewer.stop_timer()

if __name__ == '__main__':
    asyncio.run(main())