import json
import subprocess


# ==================

yt_url = ""
work_dir = ""

# ==================

origin_file = f"{work_dir}/{yt_url.split('=')[1]}.mp3"


# Download mp3 file
def download_yt_mp3():
    subprocess.run(
        f"yt-dlp -o '{origin_file}' --extract-audio --audio-format mp3 --audio-quality 256K --add-metadata --write-info-json {yt_url}",
        shell=True,
    )


# Cut by chapters
def cut_by_chapters(numbers: bool = False):
    # Find chapters in metadata
    chapters = ""
    with open(f"{origin_file}.info.json", "r") as f:
        data = json.load(f)
        chapters = data["chapters"]

    # Loop through the chapters and split the MP3 file
    for i, chapter in enumerate(chapters, start=1):
        start = chapter["start_time"]
        end = chapter["end_time"]
        title = chapter["title"].strip()

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

        subprocess.run(
            f"mp3splt -q -o '{title}' {origin_file} {start_time} {end_time}",
            shell=True,
        )


# Download video cover
def download_cover():
    subprocess.run(f"yt-dlp -o '{work_dir}/cover.jpg' --skip-download --write-thumbnail {yt_url}", shell=True)
    subprocess.run(f"mv {work_dir}/cover.jpg.webp {work_dir}/cover.jpg", shell=True)


# Remove original file and metadata
def clear():
    subprocess.run(f"rm -rf {origin_file}", shell=True)
    subprocess.run(f"rm -rf {origin_file}.info.json", shell=True)


# Main function
if __name__ == "__main__":
    subprocess.run(["clear"])
    subprocess.run(["echo", "Start"])

    download_yt_mp3()
    cut_by_chapters(True)
    download_cover()
    clear()

    subprocess.run(["echo", "Finish!"])
