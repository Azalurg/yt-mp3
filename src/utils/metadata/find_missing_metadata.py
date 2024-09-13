from mutagen.id3 import ID3, APIC
from mutagen.mp3 import MP3

from src.utils.common import get_all_songs
from src.utils.metadata.metadata import print_mp3_metadata


def get_metadata(file_path):
    try:
        audio = MP3(file_path, ID3=ID3)

        # Extract metadata
        title = audio.tags.get('TIT2', [None])[0]
        artist = audio.tags.get('TPE1', [None])[0]
        album = audio.tags.get('TALB', [None])[0]
        date = audio.tags.get('TDRC', [None])[0]
        genre = audio.tags.get('TCON', [None])[0]

        # Count images
        image_count = sum(1 for tag in audio.tags.values() if isinstance(tag, APIC))

        return [title, artist, album, date, genre, image_count]
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return [None, None, None, None, None, 0]


def find_missing_metadata(path):
    songs = get_all_songs(path)
    print(f"MP3 files found: {len(songs)}")
    count_missing = 0

    for song in songs:
        title, artist, album, date, genre, image_count = get_metadata(song)
        if not all([title, artist, album, date, genre]) or image_count == 0:
            print(song)
            if not title:
                print("Title: ", title)
            if not artist:
                print("Artist: ", artist)
            if not album:
                print("Album: ", album)
            if not date:
                print("Date: ", date)
            if not genre:
                print("Genre: ", genre)
            if image_count == 0:
                print("Covers: ", image_count)
            count_missing += 1
            print("")

    if count_missing == 0:
        print("No missing metadata found!")
    else:
        print(f"Found {count_missing} songs with missing metadata")


if __name__ == "__main__":
    path = input("Enter the path to search for missing metadata: ")
    find_missing_metadata(path)
    print("[Completed]")