import json
import subprocess


# ==================

yt_url = "https://www.youtube.com/watch?v=b1Fo_M_tj6w"
mp3_file_name = "input.mp3"

# ==================


# Download mp3 file
def download_yt_mp3():
    subprocess.run(
        f"yt-dlp -o '{mp3_file_name}' --extract-audio --audio-format mp3 --audio-quality 256K --add-metadata --write-info-json {yt_url}",
        shell=True,
    )


# Cut by chapters
def cut_by_chapters():
    # Find chapters in metadata
    chapters = ""
    with open(f"{mp3_file_name}.info.json", "r") as f:
        data = json.load(f)
        chapters = data["chapters"]

    # Loop through the chapters and split the MP3 file
    for i, chapter in enumerate(chapters, start=1):
        start = chapter["start_time"]
        end = chapter["end_time"]
        title = chapter["title"].strip()

        output_file = "{:02d}. {}".format(i, title)

        # Calculate the start time in the format required by mp3splt
        start_minutes = int(start) // 60
        start_seconds = int(start) % 60
        start_time = f"{start_minutes:02d}.{start_seconds:02d}"

        # Calculate the end time in the format required by mp3splt
        end_minutes = int(end) // 60
        end_seconds = int(end) % 60
        end_time = f"{end_minutes:02d}.{end_seconds:02d}"

        subprocess.run(
            f"mp3splt -q -o '{output_file}' {mp3_file_name} {start_time} {end_time}",
            shell=True,
        )


# Main function
if __name__ == "__main__":
    subprocess.run(["clear"])
    subprocess.run(["echo", "Start"])

    download_yt_mp3()
    cut_by_chapters()

    subprocess.run(["echo", "Finish!"])
