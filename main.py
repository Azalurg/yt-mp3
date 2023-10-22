#!/bin/python3

import json
import subprocess
import sys
import argparse


def download(yt_url: str, work_dir: str, ext: str = "mp3", q: int = 5, m: bool = False, p: bool = False):

    if ext not in ["mp3", "mp4"]:
        print(f"Wrong format: {ext}")
        exit(1)

    add_metadata = ""
    quality = f"--audio-quality {q} --audio-format mp3 --extract-audio"
    get_playlist = "--no-playlist"

    if m:
        add_metadata = "--add-metadata"

    if p:
        get_playlist = "--yes-playlist"

    if ext == "mp4":
        quality = f"-S 'height:{q}' --merge-output-format {ext}"

    query = f"yt-dlp -o '{work_dir}%(title)s.%(ext)s' {quality} {get_playlist} {add_metadata} --write-info-json {yt_url}"
    subprocess.run(query, shell=True)
    print("Downloading finished!")


# Cut by chapters
def cut_by_chapters(work_dir: str, numbers: bool = False):
    # Find chapters in metadata
    chapters = ""
    with open(f"{origin_file}.info.json", "r") as f:
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

        subprocess.run(f'mp3splt -q -o "{title}" {origin_file} {start_time} {end_time}', shell=True, )


# Download video cover
def download_cover(yt_url: str, work_dir: str):
    subprocess.run(f"yt-dlp -o '{work_dir}/cover.jpg' --skip-download --write-thumbnail {yt_url}", shell=True)
    subprocess.run(f"mv {work_dir}/cover.jpg.webp {work_dir}/cover.jpg", shell=True)


# Main function
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script description')
    parser.add_argument('-mp3', action='store_true', help='Enable MP3 option')
    parser.add_argument('-mp4', action='store_true', help='Enable MP4 option')
    parser.add_argument('--cut', action='store_true', help='Cut by chapters')
    parser.add_argument('-w', type=str, default=".", help='Specify work directory, (default: current directory)')
    parser.add_argument('-q', type=int, default=5, help='Specify quality 0-10 0: best, (default: 5)')
    parser.add_argument('--url', type=str, help='Specify YouTube URL')
    parser.add_argument('-p', action='store_true', help='Download playlist')
    parser.add_argument('-m', action='store_true', help='Download metadata')

    args = parser.parse_args()

    if args.mp3 and args.mp4:
        print("You can't use both MP3 and MP4 options")
        sys.exit()

    if not args.mp3 and not args.mp4:
        print("You need to specify MP3 or MP4 option")
        sys.exit()

    if not args.url:
        print("You need to specify YouTube URL")
        sys.exit()

    if args.w[-1] != "/":
        args.w += "/"
    # main_file += "%(title)s.%(ext)s"
    origin_file = ""

    if args.mp3:
        download(args.url, args.w, "mp3", args.q, args.m, args.p)

    if args.mp4:
        download(args.url, args.w, "mp4", args.q, args.m, args.p)

    subprocess.run(["echo", "Process finished successfully"])
