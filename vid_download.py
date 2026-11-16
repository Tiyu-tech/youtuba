from yt_dlp import YoutubeDL


def download_video(url, progress_callback=None):

    # Send download updates back to the GUI
    def progress_hook(data):

        status = data.get("status")

        if status == "downloading":
            total = data.get("total_bytes") or data.get("total_bytes_estimate")
            downloaded = data.get("downloaded_bytes", 0)

            progress = downloaded / total if total else 0

            update = {
                "status": "downloading",
                "progress": progress,
                "downloaded": downloaded,
                "total": total,
                "speed": data.get("speed"),
                "eta": data.get("eta"),
                "filename": data.get("filename"),
            }

            if progress_callback:
                progress_callback(update)

        elif status == "finished":
            if progress_callback:
                progress_callback(
                    {
                        "status": "processing",
                        "progress": 1.0,
                        "filename": data.get("filename"),
                    }
                )

    # Configure yt-dlp
    ydl_opts = {
        "format": "bestvideo+bestaudio/best",
        "outtmpl": "%(title)s.%(ext)s",
        "progress_hooks": [progress_hook],
        "merge_output_format": "mp4",
        "noplaylist": True,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            result = ydl.download([url])

        if result != 0:
            raise RuntimeError("yt-dlp could not complete the download")

        completed = {
            "status": "completed",
            "progress": 1.0,
            "message": "Download completed successfully",
        }

        if progress_callback:
            progress_callback(completed)

        return completed

    except Exception as error:
        failed = {
            "status": "error",
            "progress": 0,
            "message": str(error),
        }

        if progress_callback:
            progress_callback(failed)

        return failed


def get_video_info(url):
    with YoutubeDL({"noplaylist": True}) as ydl:
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
