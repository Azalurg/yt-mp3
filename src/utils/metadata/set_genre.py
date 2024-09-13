from mutagen.easyid3 import EasyID3

from src.utils.common import get_all_songs


def set_genre(file_path, new_genre):
    try:
        audio_file = EasyID3(file_path)
        audio_file["genre"] = new_genre
        audio_file.save()
        return 0

    except Exception as e:
        print(f"Error setting genre for {file_path}: {e}")
        return 1


if __name__ == "__main__":
    file_path = input("Enter the path to the file: ")
    new_genre = input("Enter the new genre: ")

    files = get_all_songs(file_path)
    print(f"Found {len(files)} files")
    confirm = input("Do you want to continue? [y/N]: ")
    if confirm.lower() != "y":
        print("Exiting...")
        exit(0)

    count = 0
    for file_path in files:
        count += set_genre(file_path, new_genre)

    if count == 0:
        print(f"Successfully set genre to {new_genre} for all files")
    else:
        print(f"Failed to set genre for {count} files")
    print("[Completed]")