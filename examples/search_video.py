import asyncio
from ytpy import AioYoutubeService

async def main():
    ayt = AioYoutubeService(dev_key='<replace-me>')
    
    # test search
    results = await ayt.search(q="d&e lost", 
                               search_type="video", 
                               max_results=1, 
                               part='snippet')
    print(results)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
