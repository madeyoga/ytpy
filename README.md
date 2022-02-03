# ytpy
[![CodeFactor](https://www.codefactor.io/repository/github/madeyoga/ytpy/badge)](https://www.codefactor.io/repository/github/madeyoga/ytpy)
[![Downloads](https://pepy.tech/badge/ytpy)](https://pepy.tech/project/ytpy)
![pypi-version](https://img.shields.io/pypi/v/ytpy)
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/MadeYoga/aio-ytpy/issues)
[![Discord Badge](https://discordapp.com/api/guilds/458296099049046018/embed.png)](https://discord.gg/Y8sB4ay)

Python wrapper to extract youtube data. Simple *asynchronous* wrapper to get youtube video or playlist data.
The purpose of this project is to make it easier for developers to extract data from YouTube.

## Requirements
- Python 3.x
- [Get Google API' Credential 'API KEY'](https://developers.google.com/youtube/registering_an_application) for `YoutubeDataApiV3Client` only

## Dependencies
- urllib
- aiohttp

## Install
```bash 
pip install --upgrade ytpy
```

### Usage 

```py
from ytpy import YoutubeClient
import asyncio
import aiohttp

async def main(loop):
    session = aiohttp.ClientSession()

    client = YoutubeClient(session)
    
    response = await client.search('ringtone')
    print(response)

    await session.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))

```

### Search Video by `Keywords` using YoutubeDataApiV3Client
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
from ytpy import YoutubeDataApiV3Client

async def main(loop):
    session = aiohttp.ClientSession()
    
    # Pass the aiohttp client session
    ayt =  YoutubeDataApiV3Client(session, dev_key=os.environ["DEVELOPER_KEY"])
    
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


### Examples
Check [examples](https://github.com/madeyoga/ytpy/tree/master/examples) for the full code example 


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests/examples as appropriate.
