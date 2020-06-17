from apiclient.discovery import build
from oauth2client.tools import argparser
import sys
from subprocess import call
import youtube_dl as ytdl
import asyncio
import aiohttp
import requests
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
            else: from . import config
            return config.DEVELOPER_KEY
        except DevKeyNotFoundError as e:
            raise DevKeyNotFoundError("Required 'developer_key' or credentials API key ", e)

class YoutubeVideo:
    """Represents youtube's videos attributes."""

    def __init__(self, json_=None, title="", url="", thumbnails={}, duration="", description=""):
        self.title      = title
        self.url        = url
        self.thumbnails = thumbnails
        self.duration   = duration
        self.desc       = description

    def parse(self, json_):
        self.title = json_['snippet']['title']
        self.url = "http://www.youtube.com/watch?v=" + json_['id']['videoId']
        self.thumbnails = json_['snippet']['thumbnails']
        self.desc = json_['snippet']['description']
        return self
    
    def __str__(self):
        object_to_string = "{} -- {}\n{}\n".format(self.title, self.url, self.desc)
        return object_to_string

class YoutubeService(BaseYoutubeAPI):
    """Youtube's service client."""

    def __init__(self, dev_key=""):
        super(YoutubeService, self).__init__(dev_key=dev_key)
        self.YOUTUBE_API_SERVICE_NAME = "youtube"
        self.YOUTUBE_API_VERSION = "v3"
        self.youtube = build(
            self.YOUTUBE_API_SERVICE_NAME,
            self.YOUTUBE_API_VERSION,
            developerKey=self.DEVELOPER_KEY
            )

    def search(self, keyword, max_results=7):
        """Search videos/playlist/channel by keywords."""

        search_response = self.youtube.search().list(
            q=keyword,
            part="id,snippet",
            maxResults=max_results
        ).execute()
        list_of_videos = []
        for search_result in search_response.get("items", []):
            if search_result['id']['kind'] == 'youtube#video': # #video #playlist #channel
                url = "http://www.youtube.com/watch?v=" + search_result['id']['videoId']
                title = search_result['snippet']['title']
                thumbnails = search_result['snippet']['thumbnails'] # high/medium/default
                desc = search_result['snippet']['description']
                url_detail = '{}/videos?id={}&part=contentDetails&key={}'.format(__BASE_URL__, search_result['id']['videoId'], self.DEVELOPER_KEY)
                response = requests.get(url_detail)
                response = response.json()
                vid = YoutubeVideo(
                    title=title,
                    url=url,
                    thumbnails=thumbnails,
                    duration=response['items'][0]['contentDetails']['duration'],
                    description=desc
                    )
                list_of_videos.append(vid)
            elif search_result['id']['kind'] == 'youtube#playlist':
                print(search_result)
        return list_of_videos

    def download(self, video_url="", threads=2):
        """Downloads video from given video url."""

        meta = ytdl.YoutubeDL({}).extract_info(video_url, download=False)
        quality = ''
        for fmt in meta['formats']:
            if fmt['format_note'] == '720p':
                quality = '136'
            elif fmt['format_note'] == '1080p':
                quality = '137'

        try:
            if quality != '':
                call([
                    "youtube-dl",
                    "-f " + quality + "+171",
                    video_url,
                    "--external-downloader",
                    "aria2c",
                    "--external-downloader-args",
                    "-x"+str(threads)
                ])
            else:
                call([
                    "youtube-dl",
                    video_url,
                    "--external-downloader",
                    "aria2c",
                    "--external-downloader-args",
                    "-x"+str(threads)
                ])
        except Exception as e:
            print("failed to download {}".format(video_url))
            print(e)

class AioYoutubeService(BaseYoutubeAPI):
    """Asynchronous youtube service client"""

    @staticmethod
    async def create_session():
        return aiohttp.ClientSession()

    def __init__(self, dev_key=''):
        super(AioYoutubeService, self).__init__(dev_key=dev_key)

    async def search(self, q='', search_type='video', part='snippet', max_results=7, video_category="10"):
        """Youtube search
        url: GET {BASE_URL}/search/?q=q&part=part&
        params (*)
        q       ->  stands for query, search key. default: empty string.
        part    ->  snippet, contentDetails, player, statistics, status. default: snippet
        type    ->  types: 'video', 'playlist', 'channel'. default: video.
        video_category -> 10: Music.
        returns a json response from youtube data api v3.
        """

        url = "{}/search/?key={}&q={}&type={}&part={}&maxResults={}".format(__BASE_URL__, self.DEVELOPER_KEY, q, search_type, part, max_results)
        async with aiohttp.ClientSession() as session:
            response = await session.get(url)
            search_results = await response.json()
        return search_results

    async def get_playlist(self, part="snippet", max_results=7, playlist_id="", playlist_url=""):
        """fetch playlist items
        get playlist from a given playlist_id or playlist_url.
        """

        url = "{}/playlistItems?key={}&part={}&maxResults={}&playlistId={}".format(__BASE_URL__, self.DEVELOPER_KEY, part, max_results, playlist_id)
        async with aiohttp.ClientSession() as session:
            response = await session.get(url)
            search_results = await response.json()
        return search_results

# TESTS
if __name__ == '__main__':
    async def main():
        ayt = AioYoutubeService()
        
        # test search
        results = await ayt.search(q="super junior blacksuit", search_type="video", max_results=3)
        for item in results['items']:
            vid = YoutubeVideo().parse(item)
            print(vid)
        # test get_playlist
##        results = await ayt.get_playlist(max_results=10, playlist_id="PL6GZjIxGO0cOBYqybD7-nNiA-vjF09wpC")
##        for item in results['items']:
##            print(item['snippet']['title'], item['snippet']['resourceId']['videoId'])

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
