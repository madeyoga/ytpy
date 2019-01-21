# ytpy
[![CodeFactor](https://www.codefactor.io/repository/github/madeyoga/ytpy/badge)](https://www.codefactor.io/repository/github/madeyoga/ytpy)
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/MadeYoga/youtubepy/issues)
[![Discord Badge](https://discordapp.com/api/guilds/458296099049046018/embed.png)](https://discord.gg/Y8sB4ay)

Python module for youtube services. Simple but fast `download` speed and fast `search` response. 
Of course with High Quality Video and Audio. made with youtube-dl & google api youtube data v3. 
The purpose of this project is to make it easier for developers to extract data from YouTube.

## Requirements
- Python 3.x
- [FFmpeg](https://www.ffmpeg.org/download.html)
- [Get Google API' Credential 'API KEY'](https://developers.google.com/youtube/registering_an_application)

## Dependencies
- google-api-python-client
- google-auth
- google-auth-httplib2
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
### Build YoutubeService Object
There are some ways for `YoutubeService` object to use/access your `Google Credential API key`. 
- by `dev_key`param
```py
# in your_script.py
ys = YoutubeService(
  dev_key='put your Google Credential Api key here',
  max_results=7
  )
```
- by Environment. Create an environment variable called 'DEVELOPER_KEY' and put your credential api key in it.
- by `config.py` . Create a new file called `config.py` at `youtube.py` module directory (inside `ytpy` folder).
and your put `DEVELOPER_KEY` there.

in `config.py`
```py
DEVELOPER_KEY = "put your Google Credential API key here"
```
Build `YoutubeService` Object in `your_script.py`, if you're using `Environment` or `config` method
```py
ys = YoutubeService(max_results=7)
```

### Search and Download Video
It's really simple to search and downloads videos, just use `search` and `download` method :)
```py
# Search videos by keywords
keywords='Jennie - SOLO'
search_result = ys.search(keywords)

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
  dev_key='put your Google Credential Api key here',
  max_results=7
  )

# Search videos by keywords
keywords='Jennie - SOLO'
search_result = ys.search(keywords)

# Print output
for i, video in enumerate(search_result):
  print("{}. {} - {}".format(i + 1, video.title, video.url))

# Download first entry video from `search result` list
ys.download(search_result[0].url)
# Download all search_result videos
for video in search_result:
  ys.download(video.url)
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


