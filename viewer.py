import time
import asyncio
import time
import cursor

class StatusViewer():

    def __init__(self, conn_count):

        self.line_count = conn_count + 3 

        self.conn_count = conn_count
        self.start_time = time.time()

        # cursor.hide()

        print(f'Program started...')
        print()

        for i in range(1, conn_count + 1):
            print(f'Logger {i}')

    async def _display_timer(self):

            await asyncio.sleep(1)
            elapsed_time = int(time.time() - self.start_time) 
            text = f'Program started...{elapsed_time}'
            self._update_row(1, text)
    
    def stop_timer(self):
        self.is_running = False
        elapsed_time = int(time.time() - self.start_time) 

        print()
        print(f'Program completed. Took {elapsed_time} sec.')

    async def start_timer(self):
        self.is_running = True
        while self.is_running:
            await self._display_timer()

    def update_status(self, id, text):
        new_row = (id % self.conn_count) + 1
        return self._update_row(new_row + 2, text)

    def _update_row(self, new_row, text):

        # Overwrite line
        diff = self.line_count - new_row
        print(f"\033[{diff}A\033[K{text}")

        #Move cursor to end
        new_diff = self.line_count - new_row - 1
        print(f"\033[{(new_diff)}B", end='\r')

