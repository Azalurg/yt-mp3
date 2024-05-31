import os
from pathlib import Path

from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB, TDRC, TCON
from pydub import AudioSegment
from pytube import YouTube
from pytube.exceptions import PytubeError

static_filter_params = [
    "(Official Audio)",
    "(Official Music Video)",
    "- Full album",
    "(HQ)",
    "(HD)",
    "(4K)",
    "(Vinyl RIP)",
    "(Official Video)",
    "(Official Lyric Video)",
    "(Audio)",
    "(Lyrics)",
    "(Lyric Video)",
    "(Official)",
    "(Music Video)",
    "(Video)",
    "(Full Album)",
]


class AgAudio:
    audio_path: Path

    def __init__(self, url: str, output_base: str, **kwargs):
        self.url = url
        self.output_dir_base = output_base
        self.title = kwargs.get("title", "")
        self.artist = kwargs.get("artist", "")
        self.album = kwargs.get("album", "")
        self.genre = kwargs.get("genre", "")
        self.date = kwargs.get("date", "")
        self.cover_path = kwargs.get("cover_path", "")
        self.prefix = kwargs.get("prefix", "")

        # Build output path
        self.output_dir = Path(self.output_dir_base)
        if self.genre:
            self.output_dir = self.output_dir.joinpath(self.genre)
        if self.artist:
            self.output_dir = self.output_dir.joinpath(self.artist)
        if self.album:
            if self.date:
                self.output_dir = self.output_dir.joinpath(
                    f"{self.album} ({self.date})"
                )
            else:
                self.output_dir = self.output_dir.joinpath(self.album)

        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Build filter params
        self.filter_params = static_filter_params
        self.filter_params.append(f"({self.date})")
        self.filter_params.append(f"({self.genre})")
        self.filter_params.append(f"{self.album} - ")
        self.filter_params.append(f" - {self.album}")
        self.filter_params.append(f"{self.artist} - ")
        self.filter_params.append(f" - {self.artist}")
        self.filter_params.append(f"{self.artist}- ")
        self.filter_params.append(f" -{self.artist}")

    def download(self):
        try:
            yt = YouTube(self.url)
            audio_stream = yt.streams.filter(only_audio=True).first()
            audio_path = audio_stream.download(
                output_path=self.output_dir, filename_prefix=self.prefix
            )
            self.audio_path = Path(audio_path)
            return self.audio_path
        except PytubeError as e:
            print(f"Error downloading {self.url}: {e}")
            return None

    def clean_title(self):
        if not self.title:
            self.title = self.audio_path.name

        for param in self.filter_params:
            self.title = self.title.replace(param, " ")
            self.title = self.title.replace(param.upper(), " ")

        self.title = " ".join(self.title.split())
        return self.title

    def rename(self):
        if not self.title:
            return None
        new_audio_path = self.audio_path.with_name(f"{self.title}")
        self.audio_path.rename(new_audio_path)
        self.audio_path = new_audio_path
        return self.audio_path

    def mp3_conversion(self):
        audio = AudioSegment.from_file(self.audio_path)
        mp3_path = self.audio_path.with_suffix(".mp3")
        audio.export(mp3_path, format="mp3")
        os.remove(self.audio_path)
        self.audio_path = mp3_path
        return self.audio_path

    def apply_metadata(self):
        audio_file = ID3(self.audio_path)
        audio_file.add(
            TIT2(
                encoding=3, text=os.path.splitext(os.path.basename(self.audio_path))[0]
            )
        )
        audio_file.add(TPE1(encoding=3, text=self.artist))
        audio_file.add(TALB(encoding=3, text=self.album))
        audio_file.add(TDRC(encoding=3, text=self.date))
        audio_file.add(TCON(encoding=3, text=self.genre))

        if self.cover_path:
            with open(self.cover_path, "rb") as f:
                audio_file["APIC"] = APIC(
                    encoding=3, mime="image/jpeg", type=3, desc="Cover", data=f.read()
                )
        audio_file.save()

    def perform(self):
        if self.download():
            self.mp3_conversion()
            self.clean_title()
            self.rename()
            self.apply_metadata()
        return self.audio_path


if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=PdRaUIhTmpg"
    audio = AgAudio(url, "/tmp", artist="Azalurg")
    audio.perform()
    print(audio.audio_path)
