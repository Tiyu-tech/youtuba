import customtkinter

from vid_download import download_video, get_video_info
from video_tiles import render_video_tiles


def render_mainframe(master=None):

    # Main application container
    main_frame = customtkinter.CTkFrame(master)
    main_frame.pack(side="right", fill="both", expand=True)

    render_youtube_video_form(master=main_frame)


def render_youtube_video_form(master=None):

    download_list = []

    bold_font = customtkinter.CTkFont(
        family="Arial",
        size=16,
        weight="bold",
    )

    # Form container
    youtube_video_form_frame = customtkinter.CTkFrame(
        master,
        corner_radius=15,
        border_width=2,
    )
    youtube_video_form_frame.pack(padx=20, pady=10, fill="x", expand=True)

    # Form heading
    label = customtkinter.CTkLabel(
        master=youtube_video_form_frame,
        text="Download YouTube Video",
        text_color="white",
        font=bold_font,
    )
    label.pack(padx=20, pady=10)

    # URL input
    url_input = customtkinter.CTkEntry(
        youtube_video_form_frame,
        width=320,
        height=40,
        placeholder_text="Enter YouTube video URL...",
    )
    url_input.pack(padx=20, pady=10)

    # Create the video tiles container once
    tiles_frame = render_video_tiles(
        master=master,
        download_list=download_list,
    )

    # Extract video information when the user submits a URL
    def process_video():

        url = url_input.get().strip()

        if not url:
            print("Please enter a YouTube URL.")
            return

        try:
            video_info = get_video_info(url)

            download_list.append(video_info)

            # Refresh the tiles with the newly extracted information
            render_video_tiles(
                master=master,
                download_list=download_list,
                existing_frame=tiles_frame,
            )

            url_input.delete(0, "end")

        except Exception as error:
            print(f"Error extracting video information: {error}")

    # Submit button
    submit_btn = customtkinter.CTkButton(
        master=youtube_video_form_frame,
        width=200,
        height=30,
        text="Load Video",
        command=process_video,
    )
    submit_btn.pack(padx=20, pady=10)
