# class ArCover:

import pytube
import requests


def download_youtube_thumbnail(video_url, output_path):
    try:
        # Create a YouTube object
        yt = pytube.YouTube(video_url)

        # Get the thumbnail URL
        thumbnail_url = yt.thumbnail_url
        print(f"Thumbnail URL: {thumbnail_url}")

        # Download the thumbnail image
        response = requests.get(thumbnail_url)

        # Check if the request was successful
        if response.status_code == 200:
            # Write the image content to a file
            with open(output_path, "wb") as file:
                file.write(response.content)
            print(f"Thumbnail downloaded successfully and saved to {output_path}")
        else:
            print(f"Failed to download thumbnail. Status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {e}")


# Example usage
video_url = (
    "https://www.youtube.com/watch?v=qlEoNKikrZs"  # Replace with your YouTube video URL
)
output_path = "/tmp/cover.jpg"  # Specify the output file path
download_youtube_thumbnail(video_url, output_path)
