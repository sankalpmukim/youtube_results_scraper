# Youtube Search Results 

This project uses the YouTube Data API v3 along with Django 4.0 and Django Rest Framework to store and present the data gained from search results

## Environment Variables
Make a usual .env file and put these secrets in it to make it work
 - `YOUTUBE_API_KEY_COUNT = 'x'` for the number of API keys that you have
 - `YOUTUBE_API_KEY_i = 'xyz..'` for all the `x` API keys
 - `URL = 'http://localhost:8000'` if using locally and appropriately change it if deploying
 
## Basic Features

- [x] Server should call the YouTube API continuously in background (async) with some interval (say 10 seconds) for fetching the latest videos for a predefined search query (surfing) and should store the data of videos (specifically these fields - Video title, description, publishing datetime, thumbnails URLs and any other fields you require) in a database with proper indexes.
- [x] A GET API which returns the stored video data in a paginated response sorted in descending order of published datetime.
  - `/api/videos?limit=2&offset=4`   
- [x] A basic search API to search the stored videos using their title and description.
  - `/api/videos?search=desc title` 
- [ ] Dockerize the project. (Was too focused on building features, but think it is not complicated. Used <b>pipenv</b> for dependency management.)
- [x] It should be scalable and optimised.
  - There is still room to improve but would take more time and testing. But the main cost of scaling will be the cost of Youtube API.
    - We can use an Index in published date
    - We can have a Master - Worker architecture 
  
## Bonus Points Features

- [x] Add support for supplying multiple API keys so that if quota is exhausted on one, it automatically uses the next available key. When starting the project, put API keys in .env file. After that, it will automatically manage API keys. 
    - It can also be viewed and controlled in the Admin panel.
- [x] Make a dashboard to view the stored videos with filters and sorting options. Used Django's dashboard to manage multiple aspects of the project.
- [x] Optimise search api, so that it's able to search videos containing partial match for the search query in either video title or description.
  - Ex 1: A video with title *`How to make tea?`* should match for the search query `tea how`. Works in both API and Django Admin Dashboard

## [About the project](https://www.notion.so/fampay/Backend-Assignment-FamPay-32aa100dbd8a4479878f174ad8f9d990)

This Django project is divided into broadly two main parts. 
- The REST API connected to the Videos Database
- The Data Aggregator that talks with the YouTube API and posts that information into the database.
  - Used a custom setInterval class to implement querying YouTube APi at intervals
```python
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
        
# start action every 10s
inter=setInterval(10,action)
print('just after setInterval -> time : {:.1f}s'.format(time.time()-StartTime))

# will stop interval in 25s
t=threading.Timer(25,inter.cancel)
t.start()
```
- All of this information is available at Django Admin dashboard at `/admin`
- Focus was on Modularity, Reliability and fallbacks. I believe it can be further optimized as of now.
