import time

from mutagen.easyid3 import EasyID3

from src.utils.common import get_all_songs


def print_metadata(song_path):
    audio_file = EasyID3(song_path)
    print(f"Title: {audio_file['title']}")
    print(f"Artist: {audio_file['artist']}")
    print(f"Album: {audio_file['album']}")
    print(f"Date: {audio_file['date']}")
    print(f"Genre: {audio_file['genre']}")


def append_genre(song_path: str, genre_to_add: str, detect: str = ""):
    audio_file = EasyID3(song_path)
    if 'genre' not in audio_file:
            audio_file['genre'] = []
        
    original_genre = audio_file["genre"]
    flag = True

    if detect:
        flag = False
        for genre in original_genre:
            if detect.lower() in genre.lower():
                flag = True
                break

    if genre_to_add not in original_genre and flag:
        original_genre.append(genre_to_add)

    audio_file["genre"] = original_genre
    audio_file.save()


def set_genre(song_path: str, genre: str):
    audio_file = EasyID3(song_path)
    audio_file["genre"] = genre
    audio_file.save()


if __name__ == "__main__":
    song_root = "/run/media/profil/DataBank/Music/"
    songs = get_all_songs(song_root)
    songs_amount = len(songs)
    print(f"Found {songs_amount} songs")
    count = 0
    start = time.time()
    for song in songs:
        append_genre(song, "Heavy Metal", detect="metal")
        count += 1
        if count % (songs_amount//10) == 0:
            print(f"Updated {count} songs")
            
    print(f"Updated {count} songs")
print(f" in {time.time() - start:.2f} seconds")
