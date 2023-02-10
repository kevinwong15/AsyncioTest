
import asyncio
from download import download_all
from viewer import StatusViewer


async def main():
    connect_count = 10
    status_viewer = StatusViewer(connect_count)
    asyncio.create_task(status_viewer.start_timer())
    await download_all(status_viewer, connect_count)
    status_viewer.stop_timer()


async def main2():

    connect_count = 3

    status_viewer = StatusViewer(connect_count)
    asyncio.create_task(status_viewer.start_timer())

    sem = asyncio.Semaphore(connect_count)

    async def get_page(status_viewer, sem, id, wait_time):
        async with sem:

            node_id = status_viewer.start_node(
                f'Running {id} - {wait_time} secs')
            
            await asyncio.sleep(wait_time)
            
            status_viewer.completed_count += 1
            status_viewer.release_node(
                node_id, f'Finished {id} - {wait_time} secs')

    items = [
        (1, 5),
        (2, 3),
        (3, 2),
        (4, 4),
        (5, 1),
    ]

    status_viewer.total_count = len(items)

    tasks = []

    for id, wait_time in items:
        task = asyncio.create_task(get_page(status_viewer, sem, id, wait_time))
        tasks.append(task)
    await asyncio.gather(*tasks)
    status_viewer.stop_timer()

if __name__ == '__main__':
    asyncio.run(main())
