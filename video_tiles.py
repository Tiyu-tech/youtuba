import customtkinter


def render_video_tiles(master=None, download_list=None):

    # Create the main container for all video tiles
    video_tiles_frame = customtkinter.CTkFrame(
        master,
        corner_radius=15,
        border_width=2,
    )
    video_tiles_frame.pack(padx=20, pady=10, fill="x", expand=True)

    # Add a heading above the list of videos
    heading = customtkinter.CTkLabel(
        master=video_tiles_frame,
        text="Videos Information",
        text_color="white",
        font=customtkinter.CTkFont(family="Arial", size=16, weight="bold"),
    )
    heading.pack(anchor="w", padx=20, pady=10)

    # Build a separate tile for every video in the download list
    for video in download_list or []:

        # Create the main tile that holds the thumbnail, details and button
        video_tile_frame = customtkinter.CTkFrame(
            master=video_tiles_frame,
            corner_radius=15,
            border_width=1,
        )
        video_tile_frame.pack(padx=15, pady=8, fill="x", expand=True)

        # Reserve space for the video thumbnail
        thumbnail_frame = customtkinter.CTkFrame(
            master=video_tile_frame,
            width=160,
            height=100,
            corner_radius=10,
        )
        thumbnail_frame.pack(side="left", padx=10, pady=10)
        thumbnail_frame.pack_propagate(False)

        # Show a placeholder until the actual thumbnail is loaded
        thumbnail_label = customtkinter.CTkLabel(
            master=thumbnail_frame,
            text="Thumbnail",
        )
        thumbnail_label.pack(expand=True)

        # Group the video's title and duration together
        video_info_frame = customtkinter.CTkFrame(
            master=video_tile_frame,
            fg_color="transparent",
        )
        video_info_frame.pack(side="left", padx=10, pady=10, fill="both", expand=True)

        # Display the video title
        title_label = customtkinter.CTkLabel(
            master=video_info_frame,
            text=video.get("title", "Unknown title"),
            font=customtkinter.CTkFont(family="Arial", size=14, weight="bold"),
            anchor="w",
            wraplength=400,
        )
        title_label.pack(anchor="w", pady=(5, 5))

        # Display how long the video is
        duration_label = customtkinter.CTkLabel(
            master=video_info_frame,
            text=f"Duration: {video.get('duration', 'Unknown')}",
            font=customtkinter.CTkFont(size=12),
            text_color="gray",
        )
        duration_label.pack(anchor="w")

        # Add a button for downloading this particular video
        download_button = customtkinter.CTkButton(
            master=video_tile_frame,
            text="Download",
            width=100,
        )
        download_button.pack(side="right", padx=15, pady=10)

    # Return the frame so it can be accessed or managed elsewhere
    return video_tiles_frame
