# ytpy
[![CodeFactor](https://www.codefactor.io/repository/github/madeyoga/ytpy/badge)](https://www.codefactor.io/repository/github/madeyoga/ytpy)
![pypi-version](https://img.shields.io/pypi/v/ytpy)
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

### For examples & tests
- asyncio
- aiohttp

## Install
```bash 
pip install --upgrade ytpy
```

### Run Test Code
- On project root. run command:
```python ytpy/test/test_import.py```

### Asynchronous Youtube API V3 Client
Use `AioYoutubeService` or `YoutubeApiV3Client` for asynchronous tasks.
You can pass your api key on `dev_key` param when building the object or just set your api key on environment variable named `DEVELOPER_KEY` and `AioYoutubeService` object will get it for you.
```py
import aiohttp

session = aiohttp.ClientSession()

# will get your api key from environment (named DEVELOPER_KEY).
ayt = AioYoutubeService(session)

# you can also pass it on dev_key param.
ayt = AioYoutubeService(session, dev_key='replace me')

session.close()
```

### Basic Usage: Search Video by `Search Key`
https://developers.google.com/youtube/v3/docs/search

params:
- `q`, string. Search key. default: empty string.
- `part`, string. Valid parts: snippet, contentDetails, player, statistics, status. default: snippet.
- `type`, string. Valid types: video, playlist, channel.

Example `Search` method
```py
import os
import asyncio
import aiohttp
from ytpy import YoutubeApiV3Client

async def main(loop):
    session = aiohttp.ClientSession()
    
    # Pass the aiohttp client session
    ayt = YoutubeApiV3Client(session, dev_key=os.environ["DEVELOPER_KEY"])
    
    # test search
    results = await ayt.search(q="d&e lost", 
                               search_type="video",
                               max_results=1)
    print(results)

    await session.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))
loop.close()
```

### Basic Usage: Search Video by `Search Key` (Without api key)

params:
- `q`, string. Search key. default: empty string.
- `max_results`

Example `Search` method (Without api key)
```py
from ytpy import YoutubeClient
import asyncio
import aiohttp

async def main(loop):
    session = aiohttp.ClientSession()

    client = YoutubeClient(session)
    
    response = await client.search('chico love letter')
    print(response)

    await session.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))

```

### Examples
Check [examples](https://github.com/madeyoga/ytpy/tree/master/examples) for the full code example 


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests/examples as appropriate.
