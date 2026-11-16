import customtkinter
import io
import requests
from PIL import Image


def render_video_tiles(master=None, download_list=None, existing_frame=None):

    # Reuse the existing container or create a new one
    video_tiles_frame = existing_frame or customtkinter.CTkFrame(
        master,
        corner_radius=15,
        border_width=2,
    )

    if existing_frame:
        # Clear the previous tiles before displaying the updated list
        for widget in video_tiles_frame.winfo_children():
            widget.destroy()
    else:
        video_tiles_frame.pack(padx=20, pady=10, fill="x", expand=True)

    # Add the section heading
    heading = customtkinter.CTkLabel(
        master=video_tiles_frame,
        text="Videos Information",
        text_color="white",
        font=customtkinter.CTkFont(family="Arial", size=16, weight="bold"),
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

        # Thumbnail placeholder
        thumbnail_frame = customtkinter.CTkFrame(
            master=video_tile_frame,
            width=160,
            height=100,
            corner_radius=10,
        )
        thumbnail_frame.pack(side="left", padx=10, pady=10)
        thumbnail_frame.pack_propagate(False)

        # Load and display the thumbnail image
        try:
            response = requests.get(video.get("thumbnail"))
            response.raise_for_status()
            image_data = response.content
            image = Image.open(io.BytesIO(image_data))
            image = image.resize((160, 100), Image.ANTIALIAS)
            thumbnail_image = customtkinter.CTkImage(
                light_image=image, dark_image=image
            )
            thumbnail_label = customtkinter.CTkLabel(
                master=thumbnail_frame,
                image=thumbnail_image,
                text="",
            )
            thumbnail_label.pack(fill="both", expand=True)
        except Exception as e:
            # toast error message if thumbnail fails to load
            error_label = customtkinter.CTkLabel(
                master=thumbnail_frame, text="Error loading thumbnail", text_color="red"
            )
            error_label.pack(fill="both", expand=True)

        # Video details
        video_info_frame = customtkinter.CTkFrame(
            master=video_tile_frame,
            fg_color="transparent",
        )
        video_info_frame.pack(side="left", padx=10, pady=10, fill="both", expand=True)

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
            text=f"Duration: {video.get('duration', 'Unknown')}",
            font=customtkinter.CTkFont(size=12),
            text_color="gray",
        )
        duration_label.pack(anchor="w")

        # Download button (connect its command when ready)
        download_button = customtkinter.CTkButton(
            master=video_tile_frame,
            text="Download",
            width=100,
        )
        download_button.pack(side="right", padx=15, pady=10)

    return video_tiles_frame
