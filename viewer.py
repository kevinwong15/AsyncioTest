
import time
import asyncio
import time
from collections import deque
import cursor


def seconds_to_string(s):
    _hr, remainder = divmod(s, 3600)
    _min, _sec = divmod(remainder, 60)
    text = (f'{int(_hr):02}:{int(_min):02}:{int(_sec):02}')
    return text


class StatusViewer():
    def __init__(self, conn_count):

        self.spare_line = 4

        self.completed_count = 0
        self.total_count = 0

        self.q = deque(maxlen=conn_count)
        for i in range(conn_count):
            self.q.append(i)

        self.line_count = conn_count + self.spare_line
        self.conn_count = conn_count
        self.start_time = time.time()

        cursor.hide()

        print('Program started...')
        print('Progress Bar')
        print()

        for i in range(1, conn_count + 1):
            print(f'Ready..')

    async def _display_timer(self):
        await asyncio.sleep(1)

        elapsed_secs = int(time.time() - self.start_time)

        text = f'Program running for {seconds_to_string(elapsed_secs)}... '
        self._update_row(1, text)

        if self.total_count != 0:
            text2 = f'Progress = {self.completed_count:,} out of {self.total_count:,}.'
            self._update_row(2, text2)

    def stop_timer(self):
        self.is_running = False

        elapsed_secs = int(time.time() - self.start_time)
        text = f'Program ran for {seconds_to_string(elapsed_secs)}. '
        self._update_row(1, text)

        if self.total_count != 0:
            text2 = f'Progress = {self.completed_count:,} out of {self.total_count:,}.'
            self._update_row(2, text2)

        #End
        print()
        print(f'Program completed. Took {elapsed_secs} sec.')

    async def start_timer(self):
        self.is_running = True
        while self.is_running:
            await self._display_timer()

    def start_node(self, text):
        id = self.q.popleft()
        if text != "":
            self._update_row(id + self.spare_line, text)
        return id

    def release_node(self, id, text):
        self.q.append(id)
        if text != "":
            self._update_row(id + self.spare_line, text)

    def _update_row(self, new_row, text):

        # Overwrite line
        diff = self.line_count - new_row
        print(f"\033[{diff}A\033[K{text}")

        # Move cursor to end
        new_diff = self.line_count - new_row - 1
        print(f"\033[{(new_diff)}B", end='\r')
