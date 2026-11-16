import customtkinter


def render_mainframe(master=None):
    # declare main frame
    main_frame = customtkinter.CTkFrame(master=master, corner_radius=15, border_width=2)
    # let main frame expand to fill the window and position it to the right side of the window
    main_frame.pack(
        side="right",
        fill="both",
        expand=True,
    )
    # render youtube video form
    render_youtube_video_form(master=main_frame)


def render_youtube_video_form(master=None):
    # declare youtube video form frame
    youtube_video_form_frame = customtkinter.CTkFrame(
        master,
        corner_radius=15,
        border_width=2,
        width=400,
        height=400,
    )
    youtube_video_form_frame.pack(pady=30, padx=20)
    label = customtkinter.CTkLabel(
        text="DownLoad Youtube Video",
        text_color="white",
        master=youtube_video_form_frame,
    )
