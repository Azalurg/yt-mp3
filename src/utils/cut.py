#!/bin/python3

import subprocess
import json


def cut_by_chapters(mp3_file: str, json_file: str, numbers: bool = False):
    # Find chapters in metadata
    chapters = ""
    with open(json_file, "r") as f:
        data = json.load(f)
        chapters = data["chapters"]

    # Loop through the chapters and split the MP3 file
    for i, chapter in enumerate(chapters, start=1):
        start = chapter["start_time"]
        end = chapter["end_time"]
        title = chapter["title"].strip().replace('"', "'")

        if numbers:
            title = "{:02d}. {}".format(i, title)

        # Calculate the start time in the format required by mp3splt
        start_minutes = int(start) // 60
        start_seconds = int(start) % 60
        start_time = f"{start_minutes:02d}.{start_seconds:02d}"

        # Calculate the end time in the format required by mp3splt
        end_minutes = int(end) // 60
        end_seconds = int(end) % 60
        end_time = f"{end_minutes:02d}.{end_seconds:02d}"

        print(title)

        subprocess.run(
            f'mp3splt -q -o "{title}" {mp3_file} {start_time} {end_time}',
            shell=True,
        )


if __name__ == "__main__":
    json_file = ""
    mp3_file = ""
    # cut_by_chapters(mp3_file, json_file, numbers=False)
