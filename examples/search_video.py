import asyncio

async def main():
    ayt = AioYoutubeService()
    
    # test search
    results = await ayt.search(q="d&e lost", 
                               search_type="video", 
                               max_results=1, 
                               part='snippet')
    print(results)
    for item in results['items']:
        result = await ayt.get_detail(item['id']['videoId'])
        print(result)
        break

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

