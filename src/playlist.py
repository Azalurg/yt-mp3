import os

import musicbrainzngs

from mutagen.easyid3 import EasyID3
from mutagen.id3 import APIC, ID3
from pydub import AudioSegment
from pytube import Playlist, YouTube


class AgPlaylist:
    def __init__(
        self,
        url: str,
        artist: str,
        album: str,
        genre: str = "",
        date: str = "",
        output_path: str = "/tmp",
    ):
        self.playlist_url = url
        self.artist = artist
        self.album = album
        self.date = date
        self.genre = genre
        self.main_path = output_path
        self.out_path_base = os.path.join(output_path, artist, album)
        self.music_url_list = []
        self.prefix = "{}"
        self.is_cover = False

        if self.date:
            self.out_path_base = os.path.join(output_path, artist, f"{album} ({date})")

        self.cover_path = os.path.join(self.out_path_base, "cover.jpg")
        self.songs_paths = []
        try:
            os.makedirs(self.out_path_base)
        except FileExistsError:
            pass

    def _prepare_playlist(self):
        playlist = Playlist(self.playlist_url)
        self.music_url_list = playlist.video_urls
        self.prefix = "{" + f":0{len(str(playlist.length))}" + "}. "

    def _get_cover(self):
        try:
            musicbrainzngs.set_useragent("AudioGrab", 1.0)
            result = musicbrainzngs.search_releases(
                artist=self.artist, release=self.album, limit=5
            )
            album_id = result["release-list"][0]["id"]
            cover_data = musicbrainzngs.get_image_front(album_id)

            with open(self.cover_path, "wb") as file:
                file.write(cover_data)

            self.is_cover = True

        except Exception:
            pass

    def _download_songs(self):
        for i, url in enumerate(self.music_url_list):
            yt = YouTube(url)
            video_path = (
                yt.streams.filter(file_extension="webm", type="audio")
                .order_by("abr")
                .desc()
                .first()
                .download(
                    output_path=self.out_path_base,
                    filename_prefix=self.prefix.format(i + 1),
                )
            )
            audio = AudioSegment.from_file(video_path, format="webm")
            audio.export(video_path.replace(".webm", ".mp3"), format="mp3")
            os.remove(video_path)
            print(round((i + 1) / len(self.music_url_list) * 100, 0), end="% ")
            self.songs_paths.append(video_path.replace(".webm", ".mp3"))
        print("")

    def _apply_metadata(self):
        for i, path in enumerate(self.songs_paths):
            audio_file = EasyID3(path)
            audio_file["title"] = os.path.splitext(os.path.basename(path))[0]
            audio_file["artist"] = self.artist
            audio_file["album"] = self.album
            audio_file["date"] = self.date
            audio_file["genre"] = self.genre
            audio_file["tracknumber"] = str(i + 1) + "/" + str(len(self.songs_paths))
            audio_file.save()

            if self.is_cover:
                audio_file = ID3(path)
                with open(self.cover_path, "rb") as f:
                    audio_file["APIC"] = APIC(
                        encoding=3,
                        mime="image/jpeg",
                        type=3,
                        desc="Cover",
                        data=f.read(),
                    )
                audio_file.save()

    def download(self):
        print(f"Start: {self.artist} - {self.album} ({self.date})")
        self._prepare_playlist()
        print(f"{len(self.music_url_list)} songs found")
        self._get_cover()
        print(f"Cover: {self.is_cover}")
        self._download_songs()
        print(f"{len(self.songs_paths)} songs downloaded in {self.out_path_base}")
        self._apply_metadata()
        print("Finish")
