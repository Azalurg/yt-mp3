import concurrent.futures
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

acc = 0
for playlist in playlists:
    acc += len(playlist.cover_logs)
    playlist.print_cover_logs()

if acc > 0:
    print("\n =========== \n")

acc = 0

for playlist in playlists:
    playlist.print_music_logs()
    acc += len(playlist.music_logs)

downloaded_songs = songs_sum - acc

print(
    f"{downloaded_songs}/{songs_sum} downloaded ({round(downloaded_songs/songs_sum, 4) *100}%)"
)
