import os
import time
import threading
import asyncio
import aiohttp
import platform
import requests
from data_rest_api.models import Video
from .models import ApiKey, Health
from .utils import set_api_keys


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
    try:
        Video.objects.bulk_create(items)
    except Exception as e:
        print(e)


def get_api_key():
    set_api_keys()

    api_keys = ApiKey.objects.all()
    if len(api_keys) == 0:
        return None
    for key in api_keys:
        if "error" not in execute_request(None, key=key.api_key):
            return key.api_key
        else:
            # delete that api key
            print("deleting key", key.api_key)
            key.delete()


def update_next_token(data):
    if "nextPageToken" in data.keys():
        health = Health.objects.all()
        if len(health) == 0:
            Health.objects.create(next_token=data["nextPageToken"])
        else:
            health[0].next_token = data["nextPageToken"]
            health[0].save()


def execute_request(next_token, key=None):
    print("environment key", key)
    query = None
    if os.getenv("QUERY") is not None:
        query = os.getenv("QUERY")
    else:
        query = "surfing"
    max_results = 25
    base_url = f"https://youtube.googleapis.com/youtube/v3/search?part=snippet&maxResults={max_results}&q={query}&key={key}&order=date&type=video"
    if next_token != None:
        url = f"{base_url}&pageToken={next_token}"
    else:
        url = base_url
        print("url", url)
    # async with aiohttp.ClientSession() as session:
    #     async with session.get(url) as response:
    #         data = await response.json()
    res = requests.get(url)
    data = res.json()
    update_next_token(data)
    return data


# Windows specific Event loop bug fix
if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


def get_next_token():
    # get next token from health model
    health = Health.objects.all()
    try:
        return health[0].next_token
    except Exception as e:
        return None


def execute():
    next_token = get_next_token()
    key = get_api_key()
    data = execute_request(next_token=next_token, key=key)
    post_videos(data)
