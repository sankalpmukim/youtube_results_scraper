import os
import time
import threading
import asyncio
import aiohttp
import platform
import requests
from data_rest_api.models import Video


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


next_token = None


def post_videos(data):
    items = []
    for item in data["items"]:
        post_data = {}
        post_data["id"] = item["id"]["videoId"]
        post_data["title"] = item["snippet"]["title"]
        post_data["description"] = item["snippet"]["description"]
        post_data["published_at"] = item["snippet"]["publishTime"]
        post_data["thumbnail"] = item["snippet"]["thumbnails"]["high"]["url"]
        if "nextPageToken" in data.keys():
            global next_token
            post_data["next_token"] = data["nextPageToken"]
            next_token = data["nextPageToken"]
        else:
            # end requests, deactivate the loop
            pass
        items.append(Video(**post_data))
    Video.objects.bulk_create(items)


def execute_request(next_token=None):
    print("environment key", os.getenv("YOUTUBE_API_KEY"))
    query = None
    if os.getenv("QUERY") is not None:
        query = os.getenv("QUERY")
    else:
        query = "surfing"
    base_url = f"https://youtube.googleapis.com/youtube/v3/search?part=snippet&maxResults=25&q={query}&key={os.getenv('YOUTUBE_API_KEY')}&order=date"
    if next_token is not None:
        url = f"{base_url}&pageToken={next_token}"
    else:
        url = base_url
    # async with aiohttp.ClientSession() as session:
    #     async with session.get(url) as response:
    #         data = await response.json()
    res = requests.get(url)
    data = res.json()
    if "error" not in data.keys():
        try:
            post_videos(data)
        except Exception as e:
            print(data)
        # print(e.with_traceback())
    else:
        print(data)
        # handle error
    # for response in responses:
    #     print(response.status, response)
    print("***executed successfully***")


# Windows specific Event loop bug fix
if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


def get_next_token():
    # for getting the next page token from the latest response
    if os.getenv('URL') is not None:
        url = f"{os.getenv('URL')}/api/videos?limit=1"
    else:
        return None
    response = requests.get(url)
    if response.status_code == 200:
        if len(response.json()["results"]) != 0 and "next_token" in response.json()["results"][0]:
            return response.json()["results"][0]["next_token"]
        else:
            return None


def execute():
    global next_token
    if next_token is None:
        next_token = get_next_token()
    execute_request(next_token=next_token)
