# ytpy
[![CodeFactor](https://www.codefactor.io/repository/github/madeyoga/ytpy/badge)](https://www.codefactor.io/repository/github/madeyoga/ytpy)
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/MadeYoga/aio-ytpy/issues)
[![Discord Badge](https://discordapp.com/api/guilds/458296099049046018/embed.png)](https://discord.gg/Y8sB4ay)

Python wrapper for youtube data api v3. Simple *asynchronous* wrapper to get youtube video or playlist data.
The purpose of this project is to make it easier for developers to extract data from YouTube.

- [Youtube Data API v3 documentations](https://developers.google.com/youtube/v3/docs)

## Requirements
- Python 3.x
- [Get Google API' Credential 'API KEY'](https://developers.google.com/youtube/registering_an_application)

## Dependencies
- urllib
- asyncio
- aiohttp

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
from ytpy.youtube import AioYoutubeService
```

### Asynchronous Youtube Service Object
Use `AioYoutubeService` object for asynchronous tasks.
You can pass your api key on `dev_key` param when building the object or just set your api key on environment (DEVELOPER_KEY) and `AioYoutubeService` object will automatically get it for you.
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
