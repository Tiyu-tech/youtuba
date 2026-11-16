from yt_dlp import YoutubeDL
import json


def download_video(url):
    print(url.get())


def get_video_info(url):
    with YoutubeDL() as ydl:
        info = ydl.extract_info(url, download=False)
        return {
            "title": info.get("title"),
            "thumbnail": info.get("thumbnail"),
            "duration": info.get("duration"),
            "channel": info.get("channel"),
            "views": info.get("view_count"),
            "description": info.get("description"),
            "url": url,
        }

    # process_video
