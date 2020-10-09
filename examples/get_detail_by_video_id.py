import os
import asyncio
import aiohttp
from ytpy import AioYoutubeService

async def main(loop):
    session = aiohttp.ClientSession()
    
    # Pass the aiohttp client session
    ayt = AioYoutubeService(session, dev_key=os.environ["DEVELOPER_KEY"])
    
    # test search
    results = await ayt.get_video_detail(video_id='3qhmEdMkZ1I')
    print(results)

    await session.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))
loop.close()
