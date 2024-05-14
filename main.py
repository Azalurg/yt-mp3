import concurrent.futures

from src.playlist import AgPlaylist
import json

input_file = "input.json"
max_workers = 5
playlists = []

with open(input_file, "r") as f:
    raw_data = json.load(f)

songs_sum = 0

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


with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
    executor.map(AgPlaylist.download, playlists)

print("All downloads completed!")

acc = 0
for playlist in playlists:
    acc += len(playlist.cover_logs)
    playlist.print_cover_logs()

if acc >= 0:
    print("\n =========== \n")

acc = 0

for playlist in playlists:
    playlist.print_music_logs()
    acc += len(playlist.music_logs)

downloaded_songs = songs_sum - acc

print(
    f"{downloaded_songs}/{songs_sum} downloaded ({round(downloaded_songs/songs_sum, 4) *100}%)"
)
