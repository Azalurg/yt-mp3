import concurrent.futures
import datetime
import time

from src.playlist import AgPlaylist
import json

input_file = "input.json"
max_workers = 7
playlists = []

print("Reading input file...")

with open(input_file, "r") as f:
    raw_data = json.load(f)

songs_sum = 0

print("Loading playlists...")

for rd in raw_data:
    p = AgPlaylist(
        url=rd["url"],
        artist=rd["artist"],
        album=rd["album"],
        genre=rd["genre"],
        date=rd["date"],
    )
    songs_sum += len(p.music_url_list)

    playlists.append(p)

print(f"Found {len(playlists)} playlists")
print(f"Downloading {songs_sum} songs...")
print(f"Expected time: {round(songs_sum*3.15, 2)} seconds")

with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
    executor.map(AgPlaylist.download, playlists)

print("All downloads completed!")

songs_logs = 0

with open("logs.txt", "a") as f:
    f.write(f"\n=== {datetime.datetime.now()} ===\n")
    acc = 0
    for playlist in playlists:
        acc += len(playlist.cover_logs)
        for log in playlist.cover_logs:
            f.write(log + "\n")

    if acc > 0:
        f.write("\n =========== \n")

    acc = 0
    for playlist in playlists:
        songs_logs += len(playlist.music_logs)
        for log in playlist.music_logs:
            f.write(log + "\n")

downloaded_songs = songs_sum - songs_logs

print(
    f"\n{downloaded_songs}/{songs_sum} downloaded ({round(downloaded_songs/songs_sum, 4) *100}%)"
)
