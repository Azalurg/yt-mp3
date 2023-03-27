# yt-mp3

Hi, here is script that downloads an audio file in MP3 format from a YouTube video URL provided in the script and then splits it into chapters based on the information available in the downloaded audio file's metadata.

## Dependencies:

- yt-dlp: a command-line program to download videos from YouTube.com and a few more sites.
- mp3splt: a command-line utility to split MP3 and Ogg Vorbis files without decoding.

To run the script, you need to install yt-dlp and mp3splt packages. These can be installed using the following commands on Ubuntu:

```bash
sudo apt-get install yt-dlp
sudo apt-get install mp3splt
```

## How to use the script:

1. Replace the yt_url variable with the URL of the YouTube video you want to download and split.
2. Optionally, replace the mp3_file_name variable with the name you want to give to the downloaded audio file (by default it is 'input.mp3').
3. Run the script using the following command: python script_name.py

## What the script does:

1. The script downloads the audio file in MP3 format using the yt-dlp package with the specified URL.
2. The script extracts the metadata information from the downloaded audio file and stores it in a JSON file.
3. The script reads the metadata information from the JSON file and splits the audio file into chapters using mp3splt package.
4. The script names the output files with the chapter number and the chapter title.

Note: The script requires an internet connection to download the audio file from YouTube. It also assumes that the YouTube video has chapter information in its metadata.

## Todo

- [ ] Add possibility to download playlists
- [ ] Add error handling in case the download or splitting process fails.
- [ ] Improve the user interface by allowing the user to input the YouTube URL and output file name as command-line arguments.
- [ ] Add more params to be changeable
- [ ] Check if it is possible to check work directory
- [ ] Add environment variables
- [ ] Add requirements.txt
