import os
import numpy
import librosa


def get_bpm(file_path):
    y, sr = librosa.load(file_path)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    return tempo


def categorize_mp3_files(directory):
    categories = {f"{i}": [] for i in range(60, 200, 10)}

    for filename in os.listdir(directory):  # TODO: Use walkdir
        if filename.endswith(".mp3"):
            file_path = os.path.join(directory, filename)
            bpm = get_bpm(file_path)
            bpm = int(numpy.round(bpm.item(), -1))
            c = str(bpm - bpm % 10)
            categories[c].append(filename)

    return categories


if __name__ == "__main__":
    directory = "/tmp/music/"
    categorized_files = categorize_mp3_files(directory)
    for category, files in categorized_files.items():
        if len(files) == 0:
            continue
        print(f"Category: {category}")
        print(f"Files: {files}")
        print()
