from .utils import UrlApi
from .exceptions import DevKeyNotFoundError
import json
import urllib
import os


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
            developer_key = os.environ["DEVELOPER_KEY"]
        except DevKeyNotFoundError as e:
            raise DevKeyNotFoundError("environment var 'DEVELOPER_KEY' not found.", e)

        return developer_key


class YoutubeDataApiV3Client(BaseYoutubeAPI):
    """Asynchronous youtube data api v3 client"""

    def __init__(self, aiohttp_client, dev_key=''):
        self.session = aiohttp_client

        super(YoutubeDataApiV3Client, self).__init__(dev_key=dev_key)

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

        url = self.url_api.get_playlist_url(playlist_id, part, max_results, playlist_url)

        response = await self.session.get(url)
        search_results = await response.json()
        return search_results

    async def get_related_video(self, video_id, part="snippet", max_results=7):
        url = self.url_api.get_related_url(video_id, part, max_results)

        response = await self.session.get(url)
        search_results = await response.json()

        return search_results


class YoutubeClient:
    """Asynchronous youtube client (without api key)"""

    def __init__(self, aiohttp_client, yt_music_key=None):
        self.session = aiohttp_client

        self.WATCH_URL_PREFIX = "https://www.youtube.com/watch?v="

        self.YT_URI_PREFIX = "https://www.youtube.com/results?"

        self.YT_MUSIC_URI_PREFIX = "https://music.youtube.com/youtubei/v1/search?"
        self.YT_MUSIC_KEY = yt_music_key
        self.YT_MUSIC_PAYLOAD_STRING = '{{"context":{{"client":{{"clientName":"WEB_REMIX",' \
                                       '"clientVersion":"0.1"}}}},"query":"{query}",' \
                                       '"params":"Eg-KAQwIARAAGAAgACgAMABqChADEAQQCRAFEAo="}}'

    async def search(self, q, max_results=5, language="en"):
        params = {
            "search_query": urllib.parse.quote(q),
            "hl": language,
            "persist_hl": 1
        }

        url = self.YT_URI_PREFIX + urllib.parse.urlencode(params)

        response = await self.session.get(url)
        page_content = await response.text()

        start_feature = 'ytInitialData'

        # + len(start_feature) + 3 to get rid of the start_feature & the " = "
        start_index = (page_content.index(start_feature) + len(start_feature) + 3)

        end_index = page_content.index('};', start_index)

        json_string = page_content[start_index:end_index] + '}'

        data = json.loads(json_string)

        primary_contents = data['contents']['twoColumnSearchResultsRenderer']["primaryContents"]["sectionListRenderer"][
            "contents"]

        videos = primary_contents[0]["itemSectionRenderer"]["contents"]

        results = []
        counter = 0
        for video in videos:
            res = {}
            if 'videoRenderer' in video.keys():
                video_data = video.get('videoRenderer', None)
                res["id"] = video_data.get("videoId", None)
                res["thumbnails"] = [thumb.get("url", None) for thumb in
                                     video_data.get("thumbnail", {}).get("thumbnails", [{}])]
                res["title"] = video_data.get("title", {}).get("runs", [[{}]])[0].get("text", None)
                res["long_desc"] = video_data.get("descriptionSnippet", {}).get("runs", [{}])[0].get("text", None)
                res["channel"] = video_data.get("longBylineText", {}).get("runs", [[{}]])[0].get("text", None)
                res["duration"] = video_data.get("lengthText", {}).get("simpleText", 0)
                res["views"] = video_data.get("viewCountText", {}).get("simpleText", 0)
                res["publish_time"] = video_data.get("publishedTimeText", {}).get("simpleText", 0)
                results.append(res)

                counter += 1
                if counter >= max_results:
                    break

        return results

    async def search_music(self, q):
        headers = {"Referer": "music.youtube.com"}
        params = {
            "alt": "json",
            "key": self.YT_MUSIC_KEY
        }

        response = await self.session.post(self.YT_MUSIC_URI_PREFIX + urllib.parse.urlencode(params),
                                           data=self.YT_MUSIC_PAYLOAD_STRING.format(query=q),
                                           headers=headers)

        results=[]
        response=await response.json()

        if('error' in response):
            return results

        videos=response["contents"]["sectionListRenderer"]["contents"][0]

        if "musicShelfRenderer" in videos:
            for video in videos["musicShelfRenderer"]["contents"]:
                res={}
                temp=[]
                overlay=(video['musicResponsiveListItemRenderer']["overlay"])
                res['videoId']=(overlay["musicItemThumbnailOverlayRenderer"]["content"]
                               ['musicPlayButtonRenderer']["playNavigationEndpoint"]['watchEndpoint']['videoId'])

                res['title']=(overlay["musicItemThumbnailOverlayRenderer"]["content"]['musicPlayButtonRenderer']["accessibilityPauseData"]
                             ["accessibilityData"]["label"]).split()
                res['title'].pop(0)
                res['title']=" ".join(res['title'])

                flexColumns=(video['musicResponsiveListItemRenderer']["flexColumns"][1]["musicResponsiveListItemFlexColumnRenderer"]
                            ["text"]["runs"])

                for text in flexColumns:
                    temp.append(text['text'])

                res['author']=temp.pop(0)
                res['duration']=temp.pop()

                results.append(res)

        return results
