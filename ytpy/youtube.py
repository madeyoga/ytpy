from apiclient.discovery import build
from oauth2client.tools import argparser
import sys
from subprocess import call
import youtube_dl as ytdl

class YoutubeVideo:
    def __init__(self, title="", url="", thumbnails={}, description=""):
        self.title      = title
        self.url        = url
        self.thumbnails = thumbnails
        self.desc       = description

class YoutubeService:
    def __init__(self, dev_key=""):
        if dev_key != "":
            self.DEVELOPER_KEY = dev_key
        else:
            try:
                from . import config
                self.DEVELOPER_KEY = config.DEVELOPER_KEY
            except Exception as e:
                raise ValueError('Required DEVELOPER_KEY, please set it on environment variable.')
        self.YOUTUBE_API_SERVICE_NAME = "youtube"
        self.YOUTUBE_API_VERSION = "v3"
        self.youtube = build(
            self.YOUTUBE_API_SERVICE_NAME,
            self.YOUTUBE_API_VERSION,
            developerKey=self.DEVELOPER_KEY
            )

    def search(self, keyword, max_results=7):
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
