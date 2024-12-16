
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from pytubefix import YouTube

class YouTubeDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Video Downloader")
        self.root.geometry("600x500")
        self.root.configure(bg="#121212")

        self.style = ttk.Style()
        self.style.configure("TButton", font=("Segoe UI", 14), padding=10, relief="flat", background="#1DB954", foreground="white")
        self.style.map("TButton", background=[("active", "#1ed760"), ("disabled", "#808080")])

        self.style.configure("TLabel", font=("Segoe UI", 16), background="#121212", foreground="white")
        self.style.configure("TEntry", font=("Segoe UI", 14), padding=10)
        self.style.configure("TListbox", font=("Segoe UI", 12), height=8, background="#181818", foreground="white", selectbackground="#1DB954", selectforeground="black")

        self.url_label = ttk.Label(root, text="Enter YouTube Link:")
        self.url_label.pack(pady=(30, 10))

        self.url_entry = ttk.Entry(root, width=60, font=("Segoe UI", 14))
        self.url_entry.pack(pady=10)

        self.fetch_button = ttk.Button(root, text="Fetch Streams", command=self.fetch_streams)
        self.fetch_button.pack(pady=(10, 20))

        self.stream_listbox = tk.Listbox(root, width=60, height=8, font=("Segoe UI", 12), background="#181818", fg="white", selectbackground="#1DB954", selectforeground="black")
        self.stream_listbox.pack(pady=(0, 20))

        self.download_button = ttk.Button(root, text="Download", state=tk.DISABLED, command=self.download_video)
        self.download_button.pack(pady=20)

        self.exit_button = ttk.Button(root, text="Exit", command=root.quit)
        self.exit_button.pack(pady=(10, 30))

    def fetch_streams(self):
        link = self.url_entry.get()
        
        if not link:
            messagebox.showerror("Error", "Please enter a valid YouTube URL.")
            return

        try:
            youtube = YouTube(link)
            streams = youtube.streams.filter(progressive=True)
            self.stream_listbox.delete(0, tk.END)

            for index, stream in enumerate(streams):
                self.stream_listbox.insert(tk.END, f"{index}: {stream}")

            self.download_button.config(state=tk.NORMAL)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch video details: {str(e)}")

    def download_video(self):
        try:
            selected_index = self.stream_listbox.curselection()[0]
            link = self.url_entry.get()
            youtube = YouTube(link)
            streams = youtube.streams.filter(progressive=True)

            selected_stream = streams[selected_index]
            selected_stream.download()
            messagebox.showinfo("Success", "Download successful!")

        except IndexError:
            messagebox.showerror("Error", "Please select a stream first.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloaderApp(root)
    root.mainloop()

