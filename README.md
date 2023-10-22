# yt-mp3

Hello there
This script serves as a convenient wrapper for YT-DLP, enhancing the user experience by simplifying the downloading process and reducing the need to remember multiple tags. Whether you're interested in downloading audio or video content, this tool streamlines the entire procedure. Additionally, it offers the flexibility to download entire playlists effortlessly.## Dependencies:

- yt-dlp: a command-line program to download videos from YouTube.com and a few more sites.
- mp3splt: a command-line utility to split MP3 and Ogg Vorbis files without decoding.

To run the script, you need to install yt-dlp and mp3splt packages on the os level. These can be installed using the following command on Arch:

```bash
yay -S yt-dlp mp3splt
```

## Script description

```bash
options:
  -h, --help  show this help message and exit
  -mp3        Enable MP3 option
  -mp4        Enable MP4 option
  --cut       Cut by chapters
  -w W        Specify work directory, (default: current directory)
  -q Q        Specify quality 0-10 0: best, (default: 5)
  --url URL   Specify YouTube URL
  -p          Download playlist
  -m          Download metadata
```

## Todo

- [ ] Fix mp3 splitting by chapters
- [X] Add possibility to download playlists
- [ ] Add error handling in case the download or splitting process fails.
- [X] Improve the user interface by allowing the user to input the YouTube URL and output file name as command-line arguments.
- [X] Add more params to be changeable
- [X] Check if it is possible to check work directory
- [ ] Add environment variables
- [ ] Add requirements.txt
