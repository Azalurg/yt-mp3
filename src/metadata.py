from pathlib import Path


class ArMetadata:
    def __init__(self, **kwargs):
        self.artist: str = ""
        self.title: str = ""
        self.album: str = ""
        self.genre: str = ""
        self.date: str = ""
        self.cover_path: Path = Path("")
        self.base_path: Path = Path("")
        self.audio_output_path: Path = Path("")

        for k, v in kwargs.items():
            setattr(self, k, v)

        if self.base_path:
            self.prepare_output_path()

    def prepare_output_path(self):
        if self.genre:
            self.audio_output_path = self.base_path.joinpath(self.genre)
        if self.artist:
            self.audio_output_path = self.audio_output_path.joinpath(self.artist)
        if self.album:
            if self.date:
                self.audio_output_path = self.audio_output_path.joinpath(
                    f"{self.album} ({self.date})"
                )
            else:
                self.audio_output_path = self.audio_output_path.joinpath(self.album)
        if self.title:
            self.audio_output_path = self.audio_output_path.joinpath(self.title)

    def get_dict(self):
        return {
            "artist": self.artist,
            "title": self.title,
            "album": self.album,
            "genre": self.genre,
            "date": self.date,
            "cover_path": self.cover_path,
        }
