from apiclient.discovery import build
from oauth2client.tools import argparser
import sys
from subprocess import call
import youtube_dl as ytdl
import asyncio
import aiohttp
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
            raise DevKeyNotFoundError("Required 'developer_key' or credentials API key")

class YoutubeVideo:
    """Represents youtube's videos attributes."""

    def __init__(self, title="", url="", thumbnails={}, description=""):
        self.title      = title
        self.url        = url
        self.thumbnails = thumbnails
        self.desc       = description

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
                vid = YoutubeVideo(
                    title=title,
                    url=url,
                    thumbnails=thumbnails,
                    description=desc
                    )
                list_of_videos.append(vid)
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
        return await aiohttp.ClientSession()

    def __init__(self, dev_key=''):
        super(AioYoutubeService, self).__init__(dev_key=dev_key)

    async def search(self, q='', part='snippet', raw=False):
        """Search video by keywords & parts
        url: GET {BASE_URL}/search/?q=q&part=part

        params:
        q       ->  stands for query, search key. default: empty string
        part    ->  snippet, contentDetails, player, statistics, status. default: snippet
        raw     ->  returns json type object, raw from the api response. default: False

        returns a list of YoutubeVideo Object
        """

        url = "{}/search/?q={}&part={}&key={}&maxResults=7".format(__BASE_URL__, q, part, self.DEVELOPER_KEY)
        async with aiohttp.ClientSession() as session:
            response = await session.get(url)
            search_results = await response.json()
            if raw or part!='snippet':
                return search_results
            videos = []
            for item in search_results['items']:
                if item['id']['kind'] == 'youtube#video':
                    video_url = "http://www.youtube.com/watch?v=" + item['id']['videoId']
                    ytvid = YoutubeVideo(
                        title=item['snippet']['title'],
                        url=video_url,
                        thumbnails=item['snippet']['thumbnails'],
                        description=item['snippet']['description']
                        )
                    videos.append(ytvid)
            return videos

# TESTS
if __name__ == '__main__':
    async def main():
        ays = AioYoutubeService()
        response = await ays.search(q='super junior blacksuit', part='snippet')
        print(response) # raw true
        for video in response:
            print(str(video))

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
