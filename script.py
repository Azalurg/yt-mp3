import json
import subprocess


# ==================

yt_url = "https://www.youtube.com/watch?v=b1Fo_M_tj6w"
mp3_file_name = "input.mp3"

# ==================

# Download mp3 file 
def download_yt_mp3(): 
    subprocess.run(f"yt-dlp -o '{mp3_file_name}' --extract-audio --audio-format mp3 --audio-quality 256K --add-metadata --write-info-json {yt_url}", shell=True)
    return 0

# Cut by chapters
def cut_by_chapters():
    chapters = ""
    counter = 1

    with open(f'{mp3_file_name}.info.json', 'r') as f:
        data = json.load(f)
        chapters = data["chapters"]

    # Loop through the lines and split the MP3 file
    for i, chapter in enumerate(chapters, start=1):
        start = chapter["start_time"]
        end = chapter["end_time"]
        title = chapter["title"]
        title = title.strip()

        # Calculate the start time in the format required by mp3splt
        start_minutes = int(start) // 60
        start_seconds = int(start) % 60
        start_time = f'{start_minutes:02d}.{start_seconds:02d}'

        # Calculate the end time in the format required by mp3splt
        end_minutes = int(end) // 60
        end_seconds = int(end) % 60
        end_time = f'{end_minutes:02d}.{end_seconds:02d}'

        output_file_path = '{:02d}. {}'.format(i, title)
        
        # print(f"mp3splt -q -o '{title}' {mp3_file_path} {start_time} {end_time}")
        subprocess.run(f"mp3splt -q -o '{output_file_path}' {mp3_file_name} {start_time} {end_time}", shell=True)
        counter += 1

if __name__ == "__main__":
    download_yt_mp3()
    cut_by_chapters()

    subprocess.run(["clear"])
    subprocess.run(["echo", "script finished!"])