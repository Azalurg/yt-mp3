import concurrent.futures

from src.playlist import AgPlaylist
import json

input_file = "input.json"
max_workers = 5
playlists = []

with open(input_file, "r") as f:
    raw_data = json.load(f)

for rd in raw_data:
    playlists.append(
        AgPlaylist(
            url=rd["url"],
            artist=rd["artist"],
            album=rd["album"],
            genre=rd["genre"],
            date=rd["date"],
        )
    )

print(len(playlists))

with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
    executor.map(AgPlaylist.download, playlists)

print("All downloads completed!")

for playlist in playlists:
    playlist.print_logs()
