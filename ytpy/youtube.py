from .utils import UrlApi
from .exceptions import DevKeyNotFoundError

class BaseYoutubeAPI:
    """Base Youtube API Client.
    Handles users credentials API key & URL.
    """

    def __init__(self, dev_key=''):
        self.__base_url = 'https://www.googleapis.com/youtube/v3'
        
        if dev_key != '':
            self.DEVELOPER_KEY = dev_key
        else:
            self.DEVELOPER_KEY = self.get_credential_key()

        self.url_api = UrlApi(self.DEVELOPER_KEY)

    @staticmethod
    def get_credential_key():
        """Get credentials api key from os environment.
        Set environment variable named 'DEVELOPER_KEY' and put the credentials api key there.
        """

        try:
            from . import config
        except DevKeyNotFoundError as e:
            raise DevKeyNotFoundError("environment key 'DEVELOPER_KEY' not found.", e)

        return config.DEVELOPER_KEY

class AioYoutubeService(BaseYoutubeAPI):
    """Asynchronous youtube service client"""

    def __init__(self, aiohttp_client, dev_key=''):
        self.session = aiohttp_client
            
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

        url = self.url_api.get_search_url(q, part, search_type, max_results)
        
        response = await self.session.get(url)
        search_results = await response.json()
        return search_results

    async def get_video_detail(self, video_id="", parts=['contentDetails', 'snippet']):
        """Get detail by video id"""
        
        url = self.url_api.get_detail_url(video_id, parts)
        
        response = await self.session.get(url)
        search_results = await response.json()
        return search_results
    
    async def get_playlist(self, part="snippet", max_results=7, playlist_id="", playlist_url=""):
        """fetch playlist items
        get playlist from a given playlist_id or playlist_url.
        """
    
        url = self._url_api.get_playlist_url(playlist_id, part, max_results, playlist_url)
        
        response = await self.session.get(url)
        search_results = await response.json()
        return search_results
