import os
import asyncio
import aiohttp
from ytpy import YoutubeDataApiV3Client

async def main(loop):
    session = aiohttp.ClientSession()
    
    # Pass the aiohttp client session
    ayt = YoutubeDataApiV3Client(session, dev_key=os.environ["DEVELOPER_KEY"])
    
    # test search
    results = await ayt.search(q="d&e lost", 
                               search_type="video",
                               max_results=1)
    print(results)

    await session.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))
loop.close()
