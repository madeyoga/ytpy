from ytpy import YoutubeClient
import asyncio
import aiohttp

async def main(loop):
    session = aiohttp.ClientSession()

    client = YoutubeClient(session)
    
    response = await client.search('yoasobi', language='en')
    print(response)

    await session.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))
