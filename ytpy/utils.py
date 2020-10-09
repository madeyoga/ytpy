import urllib

class UrlApi:

    def __init__(self, developer_key):
        self.__base_url = "https://www.googleapis.com/youtube/v3"
        self.__search_url = f"{self.__base_url}/search/?key={developer_key}"
        self.__detail_url = f"{self.__base_url}/videos?key={developer_key}"
        self.__playlist_url = f"{self.__base_url}/playlistItems?key={developer_key}"
    
    def get_search_url(self, query, part="snippet", search_type="10", max_results=1):
        query = urllib.parse.quote(query)
        params = '&q={}&part={}&type={}&maxResults={}'.format(query,
                                                              part,
                                                              search_type,
                                                              max_results)
        return self.__search_url + params

    def get_detail_url(self, video_id, parts):

        params = '&id={}&part={}'.format(video_id, ','.join(parts))
        return self.__detail_url + params

    def get_playlist_url(self, playlist_id, part="snippet", max_results=5, playlist_url=""):

        params = '&part={}&maxResults={}&playlistId={}'.format(part,
                                                               max_results,
                                                               playlist_id)
        return self.__playlist_url + params
