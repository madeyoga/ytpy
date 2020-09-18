class YoutubeVideo:
    """Represents youtube's videos attributes."""

    def __init__(self, json_=None, title="", url="", thumbnails={}, duration="", description=""):
        self.id         = ""
        self.title      = title
        self.url        = url
        self.thumbnails = thumbnails
        self.duration   = duration
        self.desc       = description

    def parse(self, json_):
        self.id = json_['id']['videoId']
        self.title = json_['snippet']['title']
        self.url = "http://www.youtube.com/watch?v=" + json_['id']['videoId']
        self.thumbnails = json_['snippet']['thumbnails']
        self.desc = json_['snippet']['description']
        return self
    
    def __str__(self):
        object_to_string = "{} -- {}\n{}\n".format(self.title, self.url, self.desc)
        return object_to_string
