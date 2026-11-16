import customtkinter


def render_mainframe(master=None):
    # declare main frame
    main_frame = customtkinter.CTkFrame(
        master,
    )
    # let main frame expand to fill the window and position it to the right side of the window
    main_frame.pack(
        side="right",
        fill="both",
        expand=True,
    )
    # render youtube video form
    render_youtube_video_form(master=main_frame)


def render_youtube_video_form(master=None):
    bold_font = customtkinter.CTkFont(family="Arial", size=16, weight="bold")
    # declare youtube video form frame
    youtube_video_form_frame = customtkinter.CTkFrame(
        master,
        corner_radius=15,
        border_width=2,
    )
    # youtube video from frame packing and spacing
    youtube_video_form_frame.pack(pady=30, padx=20, fill="both", expand=True)
    # Title text for form
    label = customtkinter.CTkLabel(
        text="DownLoad Youtube Video",
        text_color="white",
        master=youtube_video_form_frame,
        bg_color="transparent",
        width=30,
        height=30,
        font=bold_font,
    )
    label.pack(padx=20, pady=10)
    # input for video url
    url_input = customtkinter.CTkEntry(
        youtube_video_form_frame,
        width=320,
        height=40,
        placeholder_text="Enter YouTube video URL...",
    )
    # packing and spacing for url input
    url_input.pack(padx=20, pady=10)
    # submit Button
    submit_btn = customtkinter.CTkButton(
        master=youtube_video_form_frame, width=200, height=30, text="Download Video"
    )
    submit_btn.pack(padx=20, pady=10)
