from ytpy import YoutubeClient
import asyncio
import aiohttp
import os
from json import dumps


async def main(loop):
    session = aiohttp.ClientSession()

    client = YoutubeClient(session, yt_music_key=os.environ["YT_MUSIC_KEY"])

    response = await client.search_music(q='black suit')
    print(dumps(response, indent=2))

    await session.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))
