def main():
    import customtkinter

    # declare customtkinter app and window
    app = customtkinter.CTk()
    # Declare app title
    app.title("Youtuba Downloader")
    # declare app window size
    app.geometry("860x560")

    # declare sidebar frame
    sidebar_frame = customtkinter.CTkFrame(
        master=app, width=300, height=200, corner_radius=15, border_width=2
    )
    # sidebar frame sizing and packing
    sidebar_frame.pack(side="left", fill="y", expand=False)
    app.mainloop()


if __name__ == "__main__":
    main()
