import concurrent.futures

from src.playlist import AgPlaylist

playlists = []

max_workers = 5

with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
    executor.map(AgPlaylist.download, playlists)

print("All downloads completed!")

for playlist in playlists:
    playlist.print_logs()
