# ytpy
[![CodeFactor](https://www.codefactor.io/repository/github/madeyoga/aio-ytpy/badge)](https://www.codefactor.io/repository/github/madeyoga/aio-ytpy)
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/MadeYoga/aio-ytpy/issues)
[![Discord Badge](https://discordapp.com/api/guilds/458296099049046018/embed.png)](https://discord.gg/Y8sB4ay)

Python wrapper for youtube data api v3. Simple *asynchronous* wrapper to fetch youtube video or playlist data.

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

- importing module from your script.
```py
# depends on where you put the package/module
from ytpy.youtube import YoutubeService
```
### Build YoutubeService Object (Synchronous)
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

### Asynchronous 
Use `AioYoutubeService` object for asynchronous tasks. Its quite the same as `YoutubeService` Object. 
You can pass your api key on `dev_key` param when building the object or just set your api key on environment and `AioYoutubeService` object will automatically get it for you.
```py
# will automatically search and get your api key from environment.
_ays = AioYoutubeService()

# you can also pass it on dev_key param.
_ays = AioYoutubeService(dev_key='replace me')
```
### Asynchronous Search
params:
- `q`, string. Search key. default: empty string
- `part`, string. Valid parts: snippet, contentDetails, player, statistics, status. default: snippet.
- `raw`, boolean. If true then returns json type object, raw from the api response. If False then returns a list of `YoutubeVideo` object. default: False.

Example `Search` method
```py
ays = AioYoutubeService(dev_key='replace me')
# youtube search machine learning 
response = await ays.search(q='machine learning', part='snippet')
# output
for video in response:
  print(str(video))
```

### Example Asynchronous
```py
async def main():
    ays = AioYoutubeService()
    response = await ays.search(q='machine learning', part='snippet')
    for video in response:
        print(str(video))
    response = await ays.search(q='machine learning', part='snippet', raw=True)
    print(response) # raw true

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```

## Run youtube_downloader_example
- Open command prompt and change directory to the project path
```
C:/.../>cd 'project path'
```
- Syntax is `python example_script.py [keywords] [threads]`
```
C:/.../>python example_yt_downloader.py "forever young" 1
```
Command above will search videos from youtube with keywords "forever young"
```
C:/.../>python example_yt_downloader.py "forever young" 1
searching for: forever young
1. BLACKPINK - 'Forever Young' DANCE PRACTICE VIDEO (MOVING VER.) - http://www.youtube.com/watch?v=89kTb73csYg
2. BLACKPINK - 'FOREVER YOUNG' LYRICS (Color Coded Eng/Rom/Han) - http://www.youtube.com/watch?v=7PrxONon7jg
3. BLACKPINK - ‘FOREVER YOUNG’ 0805 SBS Inkigayo - http://www.youtube.com/watch?v=5hwepTxNKtE
4. BLACKPINK - ‘FOREVER YOUNG’ 0617 SBS Inkigayo - http://www.youtube.com/watch?v=n7ukhNJvQ8s
5. BLACKPINK - ‘FOREVER YOUNG’ 0722 SBS Inkigayo - http://www.youtube.com/watch?v=PMsBMoc9eFg
6. 【TVPP】BLACKPINK - Forever Young, 블랙핑크 – Forever Young @Show music core - http://www.youtube.com/watch?v=gH0weQOpW04
7. Alphaville - Forever Young ~Official Video - http://www.youtube.com/watch?v=t1TcDHrkQYg

eg. input `1 2 4 7`, this will download video with entry number 1 2 4 7
Choose video to download: 1
Downloading BLACKPINK - 'Forever Young' DANCE PRACTICE VIDEO (MOVING VER.)...
[youtube] 89kTb73csYg: Downloading webpage
[youtube] 89kTb73csYg: Downloading video info webpage
[youtube] 89kTb73csYg: Downloading webpage
[youtube] 89kTb73csYg: Downloading video info webpage
WARNING: Requested formats are incompatible for merge and will be merged into mkv.
[download] Destination: BLACKPINK - 'Forever Young' DANCE PRACTICE VIDEO (MOVING VER.)-89kTb73csYg.f137.mp4
[download]   9.2% of 45.16MiB at 162.40KiB/s ETA 04:18
```
