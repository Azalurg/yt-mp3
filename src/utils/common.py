import os


def get_all_songs(root_parh) -> list[str]:
    songs = []
    for root, _, files in os.walk(root_parh):
        for file in files:
            if file.endswith(".mp3"):
                songs.append(os.path.join(root, file))
    return songs


def count_songs(root_path) -> int:
    return len(get_all_songs(root_path))
