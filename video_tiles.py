import customtkinter
import io
import requests
import threading
from PIL import Image

from vid_download import download_video


def format_duration(seconds):
    if seconds is None:
        return "Unknown"

    seconds = int(seconds)
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    if hours:
        return f"{hours}h {minutes}m {seconds}s"
    elif minutes:
        return f"{minutes}m {seconds}s"
    return f"{seconds}s"


def format_speed(speed):
    if not speed:
        return "Calculating..."

    return f"{speed / (1024 * 1024):.2f} MB/s"


def start_download(video, progress_bar, status_label, download_button, master):

    # Prevent the same video from being downloaded twice
    download_button.configure(state="disabled", text="Downloading...")

    def on_progress(update):
        # Send progress updates to the main GUI thread
        master.after(
            0,
            lambda: update_download_ui(
                update,
                progress_bar,
                status_label,
                download_button,
            ),
        )

    # Download in the background to keep the GUI responsive
    threading.Thread(
        target=download_video,
        args=(video["url"], on_progress),
        daemon=True,
    ).start()


def update_download_ui(update, progress_bar, status_label, download_button):

    status = update.get("status")

    if status == "downloading":
        progress = update.get("progress", 0)
        speed = format_speed(update.get("speed"))
        eta = update.get("eta")

        progress_bar.set(progress)

        eta_text = f"{int(eta)}s remaining" if eta is not None else "Calculating..."

        status_label.configure(text=f"{progress * 100:.1f}% | {speed} | {eta_text}")

    elif status == "processing":
        progress_bar.set(1)
        status_label.configure(text="Processing video...")

    elif status == "completed":
        progress_bar.set(1)
        status_label.configure(text="Download completed!")
        download_button.configure(state="normal", text="Downloaded")

    elif status == "error":
        status_label.configure(text=f"Download failed: {update.get('message')}")
        download_button.configure(state="normal", text="Retry")


def render_video_tiles(master=None, download_list=None, existing_frame=None):

    # Reuse the existing container or create a new one
    video_tiles_frame = existing_frame or customtkinter.CTkFrame(
        master,
        corner_radius=15,
        border_width=2,
    )

    # Clear old tiles when refreshing the video list
    if existing_frame:
        for widget in video_tiles_frame.winfo_children():
            widget.destroy()
    else:
        video_tiles_frame.pack(padx=20, pady=10, fill="x", expand=True)

    # Add a heading above the video list
    heading = customtkinter.CTkLabel(
        master=video_tiles_frame,
        text="Videos Information",
        text_color="white",
        font=customtkinter.CTkFont(
            family="Arial",
            size=16,
            weight="bold",
        ),
    )
    heading.pack(anchor="w", padx=20, pady=10)

    for video in download_list or []:

        # Main tile
        video_tile_frame = customtkinter.CTkFrame(
            master=video_tiles_frame,
            corner_radius=15,
            border_width=1,
        )
        video_tile_frame.pack(padx=15, pady=8, fill="x", expand=True)

        # Thumbnail container
        thumbnail_frame = customtkinter.CTkFrame(
            master=video_tile_frame,
            width=160,
            height=100,
            corner_radius=10,
        )
        thumbnail_frame.pack(side="left", padx=10, pady=10)
        thumbnail_frame.pack_propagate(False)

        # Load the video thumbnail
        try:
            thumbnail_url = video.get("thumbnail")

            if not thumbnail_url:
                raise ValueError("Thumbnail URL not found")

            response = requests.get(thumbnail_url, timeout=10)
            response.raise_for_status()

            image = Image.open(io.BytesIO(response.content))
            image = image.convert("RGB")
            image = image.resize((160, 100), Image.Resampling.LANCZOS)

            thumbnail_image = customtkinter.CTkImage(
                light_image=image,
                dark_image=image,
                size=(160, 100),
            )

            thumbnail_label = customtkinter.CTkLabel(
                master=thumbnail_frame,
                image=thumbnail_image,
                text="",
            )
            thumbnail_label.pack(fill="both", expand=True)
            thumbnail_label.image = thumbnail_image

        except Exception as error:
            print(f"Thumbnail loading error: {error}")

            customtkinter.CTkLabel(
                master=thumbnail_frame,
                text="Thumbnail unavailable",
                text_color="red",
            ).pack(fill="both", expand=True)

        # Video details and download progress
        video_info_frame = customtkinter.CTkFrame(
            master=video_tile_frame,
            fg_color="transparent",
        )
        video_info_frame.pack(
            side="left",
            padx=10,
            pady=10,
            fill="both",
            expand=True,
        )

        title_label = customtkinter.CTkLabel(
            master=video_info_frame,
            text=video.get("title") or "Unknown title",
            font=customtkinter.CTkFont(size=14, weight="bold"),
            anchor="w",
            wraplength=400,
        )
        title_label.pack(anchor="w", pady=5)

        duration_label = customtkinter.CTkLabel(
            master=video_info_frame,
            text=f"Duration: {format_duration(video.get('duration'))}",
            font=customtkinter.CTkFont(size=12),
            text_color="gray",
        )
        duration_label.pack(anchor="w")

        # Show download status and progress
        status_label = customtkinter.CTkLabel(
            master=video_info_frame,
            text="Ready to download",
            font=customtkinter.CTkFont(size=11),
        )
        status_label.pack(anchor="w", pady=(8, 3))

        progress_bar = customtkinter.CTkProgressBar(
            master=video_info_frame,
            width=250,
        )
        progress_bar.set(0)
        progress_bar.pack(anchor="w")

        # Connect the button to this video's download
        download_button = customtkinter.CTkButton(
            master=video_tile_frame,
            text="Download",
            width=100,
        )
        download_button.configure(
            command=lambda v=video, p=progress_bar, s=status_label, b=download_button: start_download(
                v, p, s, b, master
            )
        )
        download_button.pack(side="right", padx=15, pady=10)

    return video_tiles_frame
