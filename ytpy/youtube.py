from apiclient.discovery import build
from oauth2client.tools import argparser
import sys
from subprocess import call
import youtube_dl as ytdl

class YoutubeVideo:
    def __init__(self, title="", url="", thumbnail="", description=""):
        self.title     = title
        self.url        = url
        self.thumbnail  = thumbnail
        self.desc       = description

class YoutubeService:
    def __init__(self, max_results=10, dev_key=""):
        if dev_key != "":
            self.DEVELOPER_KEY = dev_key
        else:
            try:
                from . import config
                self.DEVELOPER_KEY = config.DEVELOPER_KEY
            except Exception as e:
                try:
                    self.DEVELOPER_KEY = os.environ.get('DEVELOPER_KEY')
                except Exception as e:
                    print("Required a DEVELOPER_KEY!")
                    sys.exit(1)
        self.max_results = max_results
        self.YOUTUBE_API_SERVICE_NAME = "youtube"
        self.YOUTUBE_API_VERSION = "v3"
        self.youtube = build(
            self.YOUTUBE_API_SERVICE_NAME,
            self.YOUTUBE_API_VERSION,
            developerKey=self.DEVELOPER_KEY
            )

    def search(self, search_key):
        search_response = self.youtube.search().list(
            q=search_key,
            part="id,snippet",
            maxResults=self.max_results
        ).execute()
        list_of_videos = []
        for search_result in search_response.get("items", []):
            if search_result['id']['kind'] == 'youtube#video':
                url = "http://www.youtube.com/watch?v=" + search_result['id']['videoId']
                title = search_result['snippet']['title']
                # search_result['snippet']['thumbnails']['high'] # medium/low
                # search_result['snippet']['description']
                vid = YoutubeVideo(title=title, url=url)
                list_of_videos.append(vid)
        return list_of_videos

    def download(self, video_url="", threads=2):
        meta = ytdl.YoutubeDL({}).extract_info(video_url, download=False)
        # print(meta['formats'])
        for fmt in meta['formats']:
            if fmt['format_note'] == '720p':
                quality = '136'
            elif fmt['format_note'] == '1080p':
                quality = '137'
        try:
            call([
                "youtube-dl",
                "-f " + quality + "+171",
                video_url,
                "--external-downloader",
                "aria2c",
                "--external-downloader-args",
                "-x"+threads
            ])
        except Exception as e:
            print("failed to download {}".format(video_url))
            print(e)
