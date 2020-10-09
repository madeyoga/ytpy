import os
import asyncio
import aiohttp
from ytpy import AioYoutubeService

async def main(loop):
    session = aiohttp.ClientSession()
    
    # Pass the aiohttp client session
    ayt = AioYoutubeService(session, dev_key=os.environ["DEVELOPER_KEY"])
    
    # test search
    results = await ayt.get_related_video(video_id='x8VYWazR5mE',
                                          part='snippet',
                                          max_results=10)
    print(results)

    await session.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))
loop.close()
