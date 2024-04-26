import os

from pytube import Playlist, YouTube
from pydub import AudioSegment

playlist = Playlist("https://www.youtube.com/playlist?list=PLHTo__bpnlYVJcYxLtGqDUGqUnK0hD4FI")
url_list = playlist.video_urls
print(url_list)

prefix = "{" + f":0{len(str(playlist.length))}" + "}. "

for i, url in enumerate(url_list):
  yt = YouTube(url)
  video_path = yt.streams.filter(file_extension="webm", type="audio").order_by("abr").desc().first().download(output_path="/tmp/", filename_prefix=prefix.format(i + 1))
  audio = AudioSegment.from_file(video_path, format="webm")
  audio.export(video_path.replace(".webm", ".mp3"), format="mp3")
  os.remove(video_path)