import asyncio
import aiohttp
import urllib

if __name__ == '__main__':
    from exceptions import DevKeyNotFoundError
else:
    from .exceptions import DevKeyNotFoundError

__BASE_URL__ = 'https://www.googleapis.com/youtube/v3'

class BaseYoutubeAPI:
    """Base Youtube API Client.
    Handles users credentials API key.
    """

    def __init__(self, dev_key=''):
        self.__base_url = 'https://www.googleapis.com/youtube/v3'
        
        if dev_key != '':
            self.DEVELOPER_KEY = dev_key
        else:
            self.DEVELOPER_KEY = self.get_credential_key()

    @staticmethod
    def get_credential_key():
        """Get credentials api key from os environment.
        Set environment variable named 'DEVELOPER_KEY' and put the credentials api key there.
        """

        try:
            if __name__ == '__main__':
                import config
            else:
                from . import config
            return config.DEVELOPER_KEY
        except DevKeyNotFoundError as e:
            raise DevKeyNotFoundError("environment key 'DEVELOPER_KEY' not found.", e)

class AioYoutubeService(BaseYoutubeAPI):
    """Asynchronous youtube service client"""

    @staticmethod
    async def create_session():
        return aiohttp.ClientSession()

    def __init__(self, dev_key=''):
        super(AioYoutubeService, self).__init__(dev_key=dev_key)

    async def search(self, q='', search_type='video', part='snippet', 
                    max_results=7, video_category="10"):
        """Youtube search
        url: GET {BASE_URL}/search/?q=q&part=part&
        params:
        q       ->  stands for query, search key. default: empty string.
        part    ->  snippet, contentDetails, player, statistics, status. default: snippet
        type    ->  types: 'video', 'playlist', 'channel'. default: video.
        video_category -> 10: Music.
        
        returns a json response from youtube data api v3.
        """

        url = "{}/search/?key={}&q={}&part={}&type={}&maxResults={}".format(__BASE_URL__,
                                                                    self.DEVELOPER_KEY,
                                                                    urllib.parse.quote(q),
                                                                    part,
                                                                    search_type,
                                                                    max_results)
        async with aiohttp.ClientSession() as session:
            response = await session.get(url)
            search_results = await response.json()
        return search_results

    async def get_detail(self, video_id=""):
        request_url = "{}/videos?id={}&part=contentDetails&key={}".format(__BASE_URL__,
                                                                          video_id,
                                                                          self.DEVELOPER_KEY)
        async with aiohttp.ClientSession() as session:
            response = await session.get(request_url)
            search_results = await response.json()
        return search_results
    
    async def get_playlist(self, part="snippet", max_results=7, playlist_id="", playlist_url=""):
        """fetch playlist items
        get playlist from a given playlist_id or playlist_url.
        """
    
        url = "{}/playlistItems?key={}&part={}&maxResults={}&playlistId={}".format(__BASE_URL__,
                                                                                   self.DEVELOPER_KEY,
                                                                                   part,
                                                                                   max_results,
                                                                                   playlist_id)
        async with aiohttp.ClientSession() as session:
            response = await session.get(url)
            search_results = await response.json()
        return search_results
