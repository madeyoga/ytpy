# ytpy
[![CodeFactor](https://www.codefactor.io/repository/github/madeyoga/ytpy/badge)](https://www.codefactor.io/repository/github/madeyoga/ytpy)
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/MadeYoga/aio-ytpy/issues)
[![Discord Badge](https://discordapp.com/api/guilds/458296099049046018/embed.png)](https://discord.gg/Y8sB4ay)

Python wrapper for youtube data api v3. Simple *asynchronous* wrapper to get youtube video or playlist data.
The purpose of this project is to make it easier for developers to extract data from YouTube.

## Requirements
- Python 3.x
- [FFmpeg](https://www.ffmpeg.org/download.html)
- [Get Google API' Credential 'API KEY'](https://developers.google.com/youtube/registering_an_application)

## Dependencies
- google-api-python-client
- google-auth
- google-auth-httplib2
- oauth2client
- aiohttp
- [youtube-dl](https://github.com/rg3/youtube-dl)

## Usage
### Get Project
- Download .zip or get project module by 
```
git clone https://github.com/MadeYoga/ytpy.git
```
- Copy `ytpy` folder to your project folder

- import module.
```py
# depends on where you put the package/module
from ytpy.youtube import YoutubeService
from ytpy.youtube import AioYoutubeService
```

### Asynchronous Youtube Service Object
Use `AioYoutubeService` object for asynchronous tasks. Its quite the same as `YoutubeService` Object. 
You can pass your api key on `dev_key` param when building the object or just set your api key on environment and `AioYoutubeService` object will automatically get it for you.
```py
# will automatically search and get your api key from environment.
ayt = AioYoutubeService()

# you can also pass it on dev_key param.
ayt = AioYoutubeService(dev_key='replace me')
```
### Asynchronous Search
params:
- `q`, string. Search key. default: empty string.
- `part`, string. Valid parts: snippet, contentDetails, player, statistics, status. default: snippet.
- `type`, string. Valid types: video, playlist, channel.

Example `Search` method
```py
  ayt = AioYoutubeService()
  # test search
  results = await ayt.search(q="kpop song", search_type="video", max_results=3)
  print(results['items'][0])
```

### Example Asynchronous
```py
async def main():
  ayt = AioYoutubeService()

  # test search
  results = await ayt.search(q="super junior blacksuit", search_type="video", max_results=3)
  print(results['items'][0])

  # test get_playlist
  results = await ayt.get_playlist(max_results=10, playlist_id="PL6GZjIxGO0cOBYqybD7-nNiA-vjF09wpC")
  for item in results['items']:
      print(item['snippet']['title'], item['snippet']['resourceId']['videoId'])

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```

### Synchronous YoutubeService Object
There are some ways for `YoutubeService` object to use/access your `Google Credential API key`. 
- by `dev_key`param
```py
# in your_script.py
ys = YoutubeService(dev_key='put your Google Credential Api key here')
```
- by Environment. Create an environment variable called 'DEVELOPER_KEY' and put your credential api key in it.
- by `config.py` . Create a new file called `config.py` at `youtube.py` module directory (inside `ytpy` folder).
and your put `DEVELOPER_KEY` there.

`config.py`
```py
DEVELOPER_KEY = "put your Google Credential API key here"
```
Build `YoutubeService` Object in `your_script.py`, if you're using `Environment` or `config` method
```py
ys = YoutubeService()
```

### Search and Download Video
It's really simple to search and downloads videos, just use `search` and `download` method :)
```py
# Search videos by keywords
keywords='Jennie - SOLO'
search_result = ys.search(keyword=keywords, max_results=10)

# Print output
for i, video in enumerate(search_result):
  print("{}. {} - {}".format(i + 1, video.title, video.url))

# Download first entry video from `search result` list
ys.download(search_result[0].url)
# Download all search_result videos
for video in search_result:
  ys.download(video.url)
```

### Example, put it all together
```py
from ytpy.youtube import YoutubeService

ys = YoutubeService(
  dev_key='put your Google Credential Api key here'
  )

# Search videos by keywords
keywords='Jennie - SOLO'
search_result = ys.search(keywords, max_results=10)

# Print output
for i, video in enumerate(search_result):
  print("{}. {} - {}".format(i + 1, video.title, video.url))

# Download first entry video from `search result` list
ys.download(search_result[0].url)
# Download all search_result videos
for video in search_result:
  ys.download(video.url)
```
