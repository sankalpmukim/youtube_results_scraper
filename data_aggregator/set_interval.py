import time
import threading
import asyncio


class setInterval:
    def __init__(self, interval, action):
        self.interval = interval
        self.action = action
        self.stopEvent = threading.Event()
        thread = threading.Thread(target=self.__setInterval)
        thread.start()

    def __setInterval(self):
        nextTime = time.time()+self.interval
        while not self.stopEvent.wait(nextTime-time.time()):
            nextTime += self.interval
            self.action()

    def cancel(self):
        self.stopEvent.set()


async def execute_request(next_token=None):
    url = f"https://youtube.googleapis.com/youtube/v3/search?part=snippet&maxResults=5&q=surfing&key="
    print("Executing...")

next_token = None


def execute():
    asyncio.run(execute_request())
