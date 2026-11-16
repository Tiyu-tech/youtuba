import customtkinter

from render_mainframe import render_mainframe
from render_sidebar import render_sidebar


def main():

    # declare customtkinter app and window
    app = customtkinter.CTk()
    # Declare app title
    app.title("Youtuba Downloader")
    # declare app window size
    app.geometry("860x560")
    # render main frame
    render_mainframe(master=app)
    # render sidebar frame
    render_sidebar(master=app)
    app.mainloop()


if __name__ == "__main__":
    main()
