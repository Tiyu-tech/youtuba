import customtkinter


def render_mainframe(master=None):
    # declare main frame
    main_frame = customtkinter.CTkFrame(master=master, corner_radius=15, border_width=2)
    main_frame.pack(side="right", fill="both", expand=True)
