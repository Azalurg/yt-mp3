import time

from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TDRC, TCON, APIC
from src.utils.common import get_all_songs


def print_mp3_metadata(file_path):
    try:
        audio = MP3(file_path, ID3=ID3)

        # Extract metadata
        title = audio.tags.get('TIT2', ['Unknown Title'])[0]
        artist = audio.tags.get('TPE1', ['Unknown Artist'])[0]
        album = audio.tags.get('TALB', ['Unknown Album'])[0]
        date = audio.tags.get('TDRC', ['Unknown Date'])[0]
        genre = audio.tags.get('TCON', ['Unknown Genre'])[0]

        # Count images
        image_count = sum(1 for tag in audio.tags.values() if isinstance(tag, APIC))

        # Print metadata
        print(f"Title: {title}")
        print(f"Artist: {artist}")
        print(f"Album: {album}")
        print(f"Date: {date}")
        print(f"Genre: {genre}")
        print(f"Number of images: {image_count}")

    except Exception as e:
        print(f"Error processing {file_path}: {e}")



def append_genre(song_path: str, genre_to_add: str, detect: str = ""):
    audio_file = EasyID3(song_path)
    if "genre" not in audio_file:
        audio_file["genre"] = []

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
        if count % (songs_amount // 10) == 0:
            print(f"Updated {count} songs")

    print(f"Updated {count} songs")
    print(f" in {time.time() - start:.2f} seconds")
