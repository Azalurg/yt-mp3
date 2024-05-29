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
print(f"Expected time: {len(raw_data)} seconds")
time_start = time.time()
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
print(f"Initialization time: {round(time.time() - time_start, 2)} seconds")
print(f"Expected time: {round(songs_sum*2.65, 2)} seconds")

stat_time = time.time()

with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
    executor.map(AgPlaylist.download, playlists)

print("All downloads completed!")
print(f"Downloading time: {round(time.time() - stat_time, 2)} seconds")

songs_logs = 0

with open("logs.txt", "a") as f:
    f.write(f"\n=== {datetime.datetime.now()} ===\n")
    f.write("COVERS:\n")
    i = 1
    for playlist in playlists:
        for log in playlist.cover_logs:
            f.write(f"{i:02}. {log.info}\n")
            i += 1
    f.write("\n =========== \n")
    f.write("SONGS:\n")
    i = 1
    for playlist in playlists:
        songs_logs += len(playlist.music_logs)
        for log in playlist.music_logs:
            f.write(f"{i:02}. {log.info}\n")
            i += 1

with open("urls.txt", "a") as f:
    for playlist in playlists:
        for log in playlist.music_logs:
            f.write(f"{log.url}\n")

downloaded_songs = songs_sum - songs_logs

print(
    f"\n{downloaded_songs}/{songs_sum} downloaded ({round(downloaded_songs/songs_sum, 4) *100}%)"
)
