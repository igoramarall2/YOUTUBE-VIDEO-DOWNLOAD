import customtkinter
import os
import ffmpeg
import threading
from PIL import Image
import youtube_dl
import tkinter
import tkinter.messagebox
import customtkinter as ctk
from pytube import Playlist
from pytube import YouTube
from tkinter import filedialog

# pyinstaller --onedir --windowed --add-data "C:\Users\igora\AppData\Local\Programs\Python\Python311\Lib\site-packages\customtkinter;customtkinter" youtube_video_download.py


class App(customtkinter.CTk):
    def __init__(self):  # sourcery skip: avoid-builtin-shadow
        super().__init__()

        self.title("Pytuber Downloder")
        self.geometry("760x450")
        self.resizable(False, False)
        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        # Setting icon of master window
        photo = tkinter.PhotoImage(
            # file=r"C:\Users\igora\AppData\Local\Programs\Python\Python311\Lib\site-packages\customtkinter\icon.png"
            file=r"D:\Python\YOUTUBE VIDEO DOWNLOAD\icon.png"
        )
        self.wm_iconphoto(False, photo)
        url_var = tkinter.StringVar()

        def optionmenu_callback(quality):
            global download_quality
            download_quality = ""
            if quality == "4k":
                download_quality = "4k"
                print("Downloading in 4K")
            if quality == "1080p":
                download_quality = "1080p"
                print("Downloading in 1080p")
            if quality == "720p":
                download_quality = "720p"
                print("Downloading in 720p")
            if quality == "480p":
                download_quality = "480p"
                print("Downloading in 480p")

        def videos_thread():
            t1 = threading.Thread(target=videos)
            t1.start()

        def playlist_thread():
            t2 = threading.Thread(target=playlist)
            t2.start()

        def multiplas_playlists_thread():
            t3 = threading.Thread(target=multiplas_playlists)
            t3.start()

        def audio_only_thread():
            t4 = threading.Thread(target=audio_only)
            t4.start()

        def videos():
            url_video = url_var.get()
            filedir = filedialog.askdirectory(
                initialdir="/",
                title="SELECIONE O LOCAL DE DOWNLOAD",
            )
            print(filedir)
            path_file = filedir
            yt = YouTube(url_video)
            self.video_box_frame.insert(text=f"Downloading: {yt.title}\n", index="0.0")
            # self.video_box_frame.get("0.0", "end")

            video_title = yt.title.replace("/", "_")
            video_title2 = yt.title.replace("|", "_")

            print(f"Downloading: {video_title2}")

            # yt.streams.get_highest_resolution().download(path_file) #versao para maior resolucao

            temp_video = yt.streams.filter(res="1080p", progressive=False)
            temp_video.first().download(
                output_path=path_file, filename=f"{video_title2}.mp4"
            )
            temp_audio = yt.streams.get_audio_only()
            temp_audio.download(
                output_path=path_file, filename=f"mp3 {video_title2}.mp4"
            )
            # https://www.youtube.com/watch?v=uEJ-Rnm2yOE

            print(f"{path_file}{video_title2}.mp4")
            print(f"{path_file}mp3 {video_title2}.mp4")

            os.rename(
                f"{path_file}{video_title2}.mp4",
                f"{path_file}{video_title2} video_temp.mp4",
            )
            os.rename(
                f"{path_file}mp3 {video_title2}.mp4",
                f"{path_file}{video_title2} audio_temp.mp4",
            )

            video_input = ffmpeg.input(f"{path_file}{video_title2} video_temp.mp4")
            audio_input = ffmpeg.input(f"{path_file}{video_title2} audio_temp.mp4")

            print(video_input)
            print(audio_input)

            ffmpeg.concat(
                video_input,
                audio_input,
                v=1,
                a=1,
            ).output(f"{path_file}1080p {video_title2}.mp4", vcodec="libx265").run()

            os.remove(f"{path_file}{video_title2} video_temp.mp4")
            os.remove(f"{path_file}{video_title2} audio_temp.mp4")

            os.rename(
                f"{path_file}1080p {video_title2}.mp4", f"{path_file}{video_title2}.mp4"
            )

            self.video_box_frame.insert(text=f"Downloaded: {yt.title}\n", index="end")
            # self.video_box_frame.get("0.0", "end")
            print("Done")

        def playlist():
            url_playlist = url_var.get()
            p = Playlist(url_playlist)
            filedir = filedialog.askdirectory(
                initialdir="/",
                title="SELECIONE O LOCAL DE DOWNLOAD",
            )
            print(filedir)
            path_file = filedir
            folder_name = str(p.title)
            print(f"Downloading Playlist: {p.title}")
            print("#" * 60)
            for video in p.videos:
                print(f"Downloading: {video.title}")
                self.playlist_textbox.insert(text=f"Downloading: {video.title}\n")
                self.playlist_textbox.get("end")

                video.streams.get_highest_resolution().download(
                    output_path=path_file + "\\" + folder_name
                )
                print("-" * 60)

        def multiplas_playlists():
            lista_playlists = []
            url_playlist = str(url_var.get())
            lista_playlists.extend(url_playlist.split(","))
            print(lista_playlists)
            filedir = filedialog.askdirectory(
                initialdir="/",
                title="SELECIONE O LOCAL DE DOWNLOAD",
            )
            print(filedir)
            path_file = filedir
            for p in lista_playlists:
                url = p
                playlist = Playlist(url)
                print(playlist.title)
                folder_name = str(playlist.title)
                print(p)
                print("###" * 30)
                for i in playlist.videos:
                    print(f"Downloading: {i.title}")
                    self.url_lista_playlists.insert(text=f"Downloading: {i.title}\n")
                    self.url_lista_playlists.get("0.0", "end")
                    i.streams.get_highest_resolution().download(
                        output_path=path_file + "\\" + folder_name
                    )
                    print(
                        "----------------------------------------------------------------"
                    )

        def audio_only():
            url_playlist = url_var.get()
            filedir = filedialog.askdirectory(
                initialdir="/",
                title="SELECIONE O LOCAL DE DOWNLOAD",
            )
            print(filedir)
            path_file = filedir
            video_url = url_playlist
            video_info = youtube_dl.YoutubeDL().extract_info(
                url=video_url, download=False
            )
            filename = f"{video_info['title']}.mp3"
            options = {
                "format": "bestaudio/best",
                "keepvideo": False,
                "outtmpl": f"{path_file}\\{filename}",
                "verbose": True,
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }
                ],
                "prefer_ffmpeg": True,
            }
            with youtube_dl.YoutubeDL(options) as ydl:
                ydl.download([video_info["webpage_url"]])
            print(f"Download complete... {filename}")

        # load images with light and dark mode image
        image_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            r"D:\Python\YOUTUBE VIDEO DOWNLOAD\test\manual_integration_tests\test_images",
        )
        self.logo_image = customtkinter.CTkImage(
            Image.open(os.path.join(image_path, "icon.png")),
            size=(26, 26),
        )
        self.large_test_image = customtkinter.CTkImage(
            Image.open(os.path.join(image_path, "large_test_image.png")),
            size=(500, 150),
        )
        self.image_icon_image = customtkinter.CTkImage(
            Image.open(os.path.join(image_path, "image_icon_light.png")), size=(20, 20)
        )
        self.home_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "home_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "home_light.png")),
            size=(20, 20),
        )
        self.chat_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "chat_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "chat_light.png")),
            size=(20, 20),
        )
        self.add_user_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "add_user_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "add_user_light.png")),
            size=(20, 20),
        )

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(5, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(
            self.navigation_frame,
            text="  Pytube Download",
            image=self.logo_image,
            compound="left",
            font=customtkinter.CTkFont(size=15, weight="bold"),
        )
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        # home
        self.home_button = customtkinter.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Video",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.home_image,
            anchor="w",
            command=self.home_button_event,
        )
        self.home_button.grid(row=1, column=0, sticky="ew")

        # frame2
        self.frame_2_button = customtkinter.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Playlist",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.chat_image,
            anchor="w",
            command=self.frame_2_button_event,
        )
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        # frame3
        self.frame_3_button = customtkinter.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Lista de Playlists",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.add_user_image,
            anchor="w",
            command=self.frame_3_button_event,
        )
        self.frame_3_button.grid(row=3, column=0, sticky="ew")

        # frame4
        self.frame_4_button = customtkinter.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Audio",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.add_user_image,
            anchor="w",
            command=self.frame_4_button_event,
        )
        self.frame_4_button.grid(row=4, column=0, sticky="ew")

        # appearance_mode_menu
        self.appearance_mode_menu = customtkinter.CTkOptionMenu(
            self.navigation_frame,
            values=["Light", "Dark", "System"],
            command=self.change_appearance_mode_event,
        )
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # create video frame
        self.video_download = customtkinter.CTkFrame(
            self, corner_radius=0, fg_color="transparent"
        )
        self.video_download.grid_columnconfigure(0, weight=1)

        self.video_box_frame = customtkinter.CTkTextbox(
            self.video_download, width=250, height=300
        )
        self.video_box_frame.grid(
            row=1, column=0, padx=(20, 20), pady=(5, 5), sticky="nsew"
        )
        # self.video_box_frame.configure(state="disabled")

        self.label_1 = ctk.CTkLabel(self.video_download)
        self.label_1.place(relx=0.5, rely=0.5, anchor=tkinter.E)
        self.label_1.configure(text="URL DO VIDEO")
        self.label_1.grid(row=3, column=0, padx=(0, 0), pady=(0, 0), sticky="nsew")

        self.entry = customtkinter.CTkEntry(
            self.video_download, placeholder_text="URL", textvariable=url_var
        )
        self.entry.grid(row=4, column=0, padx=(20, 20), pady=(0, 0), sticky="nsew")

        self.video_download_button_4 = customtkinter.CTkButton(
            self.video_download, text="DOWNLOAD", anchor="S", command=videos_thread
        )
        self.video_download_button_4.grid(
            row=7, column=0, padx=20, pady=10, sticky="ns"
        )

        self.combobox = customtkinter.CTkOptionMenu(
            self.video_download,
            values=["4k", "1080p", "720p", "480p"],
            command=optionmenu_callback,
            width=70,
        )
        self.combobox.grid(row=7, column=0, padx=20, pady=10, sticky="nse")
        self.combobox.set("Download")  # set initial value
        self.combobox.get()  # set initial valuee

        # create playlist frame
        self.playlist = customtkinter.CTkFrame(
            self, corner_radius=0, fg_color="transparent"
        )
        self.playlist.grid_columnconfigure(0, weight=1)

        self.playlist_textbox = customtkinter.CTkTextbox(
            self.playlist, width=250, height=300
        )
        self.playlist_textbox.grid(
            row=2, column=0, padx=(20, 20), pady=(5, 5), sticky="nsew"
        )

        self.label_1 = ctk.CTkLabel(self.playlist)
        self.label_1.place(relx=0.5, rely=0.5, anchor=tkinter.E)
        self.label_1.configure(text="URL DO VIDEO")
        self.label_1.grid(row=3, column=0, padx=(0, 0), pady=(0, 0), sticky="nsew")

        self.entry = customtkinter.CTkEntry(
            self.playlist, placeholder_text="URL", textvariable=url_var
        )
        self.entry.grid(row=4, column=0, padx=(20, 20), pady=(0, 0), sticky="nsew")

        self.video_download_button_4 = customtkinter.CTkButton(
            self.playlist,
            text="DOWNLOAD",
            anchor="S",
            command=playlist_thread,
        )
        self.video_download_button_4.grid(row=7, column=0, padx=20, pady=10)

        # create lista_playlists frame
        self.lista_playlists = customtkinter.CTkFrame(
            self, corner_radius=0, fg_color="transparent"
        )
        self.lista_playlists.grid_columnconfigure(0, weight=1)

        self.url_lista_playlists = customtkinter.CTkTextbox(
            self.lista_playlists,
            width=250,
            height=300,
        )
        self.url_lista_playlists.grid(
            row=2, column=0, padx=(20, 20), pady=(5, 5), sticky="nsew"
        )
        self.url_lista_playlists.get("0.0", "end")

        self.label_1 = ctk.CTkLabel(self.lista_playlists)
        self.label_1.place(relx=0.5, rely=0.5, anchor=tkinter.E)
        self.label_1.configure(text="URL DO VIDEO")
        self.label_1.grid(row=3, column=0, padx=(0, 0), pady=(0, 0), sticky="nsew")

        self.entry = customtkinter.CTkEntry(
            self.lista_playlists, placeholder_text="URL", textvariable=url_var
        )
        self.entry.grid(row=4, column=0, padx=(20, 20), pady=(0, 0), sticky="nsew")

        self.video_download_button_4 = customtkinter.CTkButton(
            self.lista_playlists,
            text="DOWNLOAD",
            anchor="S",
            command=multiplas_playlists_thread,
        )
        self.video_download_button_4.grid(row=5, column=0, padx=20, pady=10)

        # create audio frame
        self.audio = customtkinter.CTkFrame(
            self, corner_radius=0, fg_color="transparent"
        )
        self.audio.grid_columnconfigure(0, weight=1)

        self.textbox = customtkinter.CTkTextbox(self.audio, width=250, height=100)
        self.textbox.grid(row=2, column=0, padx=(20, 20), pady=(5, 5), sticky="nsew")

        self.entry = customtkinter.CTkEntry(self.audio, placeholder_text="URL")
        self.entry.grid(row=3, column=0, padx=(20, 20), pady=(20, 0), sticky="nsew")

        self.video_download_button_4 = customtkinter.CTkButton(
            self.audio, text="DOWNLOAD", anchor="S", command=audio_only_thread
        )
        self.video_download_button_4.grid(row=5, column=0, padx=20, pady=10)

        # select default frame
        self.select_frame_by_name("home")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(
            fg_color=("gray75", "gray25") if name == "home" else "transparent"
        )
        self.frame_2_button.configure(
            fg_color=("gray75", "gray25") if name == "frame_2" else "transparent"
        )
        self.frame_3_button.configure(
            fg_color=("gray75", "gray25") if name == "frame_3" else "transparent"
        )
        self.frame_4_button.configure(
            fg_color=("gray75", "gray25") if name == "frame_4" else "transparent"
        )

        # show selected frame
        if name == "home":
            self.video_download.grid(row=0, column=1, sticky="nsew")
        else:
            self.video_download.grid_forget()
        if name == "frame_2":
            self.playlist.grid(row=0, column=1, sticky="nsew")
        else:
            self.playlist.grid_forget()
        if name == "frame_3":
            self.lista_playlists.grid(row=0, column=1, sticky="nsew")
        else:
            self.lista_playlists.grid_forget()
        if name == "frame_4":
            self.audio.grid(row=0, column=1, sticky="nsew")
        else:
            self.audio.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")

    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")

    def frame_4_button_event(self):
        self.select_frame_by_name("frame_4")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)


if __name__ == "__main__":
    app = App()
    app.mainloop()
