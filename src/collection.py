import os
from typing import List

from pydub import AudioSegment
from pytube import YouTube

from src.audio import ArAudio
from src.metadata import ArMetadata


class ArChapter:
    def __init__(self, title: str, start: int, end):
        self.title = title
        self.start = start
        self.end = end

    def __str__(self):
        return f"{self.title} - {self.start} - {self.end}"


class ArCollection:
    def __init__(self, url: str, metadata: ArMetadata = ArMetadata()):
        self.url = url
        self.yt = YouTube(url)
        self.data = self.yt.initial_data
        self.chapters: List[ArChapter] = []
        self.audio_path = ""
        self.metadata = metadata

    def find_it(self, source: dict, key: str):
        if key in source:
            return source[key]
        for k, v in source.items():
            if isinstance(v, dict):
                item = self.find_it(v, key)
                if item:
                    return item
        return None

    def get_chapters(self):
        raw_chapters = self.data["engagementPanels"][1][
            "engagementPanelSectionListRenderer"
        ]["content"]["macroMarkersListRenderer"]["contents"]
        for c in raw_chapters:
            title = c["macroMarkersListItemRenderer"]["title"]["simpleText"]
            start = self.find_it(c, "startTimeSeconds") or 0
            self.chapters.append(ArChapter(title, start, 0))
        for i, c in enumerate(self.chapters):
            if i + 1 < len(self.chapters):
                c.end = self.chapters[i + 1].start
            else:
                c.end = self.yt.length

    def download_audio(self):
        self.audio_path = ArAudio(
            audio_url=self.url,
            output_base="/tmp/music",
            **self.metadata.get_dict()
        ).perform()

    def cut_audio(self):
        for c in self.chapters:
            audio = AudioSegment.from_file(self.audio_path, format="mp3")
            audio = audio[c.start * 1000 : c.end * 1000]
            audio.export(f"/tmp/music{c.title}.mp3", format="mp3")
        os.remove(self.audio_path)

    def perform(self):
        self.get_chapters()
        self.download_audio()
        self.cut_audio()
        return 0


if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=b1Fo_M_tj6w"
    ac = ArCollection(url)
    print(ac.perform())
