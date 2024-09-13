from mutagen.easyid3 import EasyID3

from src.utils.common import get_all_songs


def add_genre(file_path, genre_to_add):
    try:
        audio_file = EasyID3(file_path)
        if "genre" not in audio_file:
            audio_file["genre"] = []

        original_genre = audio_file["genre"]
        if genre_to_add not in original_genre:
            original_genre.append(genre_to_add)

        audio_file["genre"] = original_genre
        audio_file.save()
        return 0

    except Exception as e:
        print(f"Error setting genre for {file_path}: {e}")
        return 1


if __name__ == "__main__":
    file_path = input("Enter the path to the file: ")
    new_genre = input("Enter genre to add: ")

    files = get_all_songs(file_path)
    print(f"Found {len(files)} files")
    confirm = input("Do you want to continue? [y/N]: ")
    if confirm.lower() != "y":
        print("Exiting...")
        exit(0)

    count = 0
    for file_path in files:
        count += add_genre(file_path, new_genre)

    if count == 0:
        print(f"Successfully add genre {new_genre} for all files")
    else:
        print(f"Failed to add genre for {count} files")
    print("[Completed]")
