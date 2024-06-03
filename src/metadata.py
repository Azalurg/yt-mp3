class ArMetadata:
    artist: str
    time: str
    title: str
    album: str
    genre: str
    date: str
    cover: str

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def get_dict(self):
        return {
            "artist": self.artist,
            "time": self.time,
            "title": self.title,
            "album": self.album,
            "genre": self.genre,
            "date": self.date,
            "cover": self.cover,
        }