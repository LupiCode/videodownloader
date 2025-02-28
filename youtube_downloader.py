import yt_dlp
import tkinter as tk
from tkinter import filedialog, messagebox

def download_video():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Error", "Please enter a video URL")
        return
    
    save_path = filedialog.askdirectory()
    if not save_path:
        return  # User canceled folder selection
    
    # Check if audio-only mode is selected
    audio_only = audio_checkbox_var.get()

    # Set download options
    if audio_only:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f"{save_path}/%(title)s.%(ext)s",
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'progress_hooks': [progress_hook]
        }
    else:
        ydl_opts = {
            'format': 'best',
            'outtmpl': f"{save_path}/%(title)s.%(ext)s",
            'progress_hooks': [progress_hook]
        }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        messagebox.showinfo("Success", "Download complete!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def progress_hook(d):
    if d['status'] == 'downloading':
        status_label.config(text=f"Downloading: {d['_percent_str']} at {d['_speed_str']}")
    elif d['status'] == 'finished':
        status_label.config(text="Download complete!")

# GUI Setup
root = tk.Tk()
root.title("Video Downloader")

tk.Label(root, text="Enter Video URL:").pack(pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

# Audio Only Option
audio_checkbox_var = tk.BooleanVar()
audio_checkbox = tk.Checkbutton(root, text="Download Audio Only", variable=audio_checkbox_var)
audio_checkbox.pack(pady=5)

download_button = tk.Button(root, text="Download Video", command=download_video)
download_button.pack(pady=10)

status_label = tk.Label(root, text="", fg="blue")
status_label.pack()

root.mainloop()
