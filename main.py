import json
import subprocess
import sys
import argparse


def download_yt_mp3(yt_url: str, output: str, audio_format: str = "mp3", audio_quality: int = 5):
    subprocess.run(
        f"yt-dlp -o '{output}' -S +res:144 --extract-audio --audio-format {audio_format} --audio-quality {audio_quality} --add-metadata --write-info-json {yt_url}",
        shell=True, )
    print("Downloading finished!")
    

def download_yt_mp4(yt_url: str, output: str, video_format: str = "mp4", video_quality: int = 1080):
    query = f"yt-dlp -o '{output}' -S 'height:{video_quality}' --merge-output-format {video_format} --add-metadata --write-info-json {yt_url}"
    subprocess.run(query, shell=True)
    print("Downloading finished!")


# Cut by chapters
def cut_by_chapters(work_dir:str, numbers: bool = False):
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
def download_cover(work_dir: str):
    subprocess.run(f"yt-dlp -o '{work_dir}/cover.jpg' --skip-download --write-thumbnail {yt_url}", shell=True)
    subprocess.run(f"mv {work_dir}/cover.jpg.webp {work_dir}/cover.jpg", shell=True)


# Remove original file and metadata
def cleaner(work_dir: str, main_file:str, chapters: bool):
    subprocess.run(f"rm -rf {main_file}.info.json", shell=True)
    if chapters:
        subprocess.run(f"rm -rf {main_file}", shell=True)
    print("Cleaning finished")


# Main function
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Description of your script')
    parser.add_argument('-mp3', action='store_true', help='Enable MP3 option')
    parser.add_argument('-mp4', action='store_true', help='Enable MP4 option')
    parser.add_argument('-w', type=str, default=".", help='Specify work directory, (default: current directory)')
    parser.add_argument('-q', type=int, default=5, help='Specify quality 0-10 0: best, (default: 5)')
    parser.add_argument('--url', type=str, help='Specify YouTube URL')
    parser.add_argument('-c', action='store_true', help='Cut by chapters (default: 5)')


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
        origin_file = f"{args.w}{args.url.split('=')[1]}.mp3"
        download_yt_mp3(args.url, origin_file, audio_quality=args.q)
        if args.c:
            cut_by_chapters(args.w, True)
            download_cover(args.w)
            
    elif args.mp4:
        origin_file = f"{args.w}{args.url.split('=')[1]}.mp4"
        if args.q >= 8:
            args.q = 1080
        elif args.q >= 6:
            args.q = 720
        elif args.q >= 4:
            args.q = 480
            
        download_yt_mp4(args.url, origin_file, video_quality=args.q)
        if args.c:
            cut_by_chapters(true)

    cleaner(args.w, origin_file, args.c)

    subprocess.run(["echo", "Process finished successfully"])
