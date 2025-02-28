import yt_dlp

def download_video(video_url, output_path="downloads/%(title)s.%(ext)s"):
    ydl_opts = {
        'format': 'best',  # Download the best available quality
        'outtmpl': output_path,  # Save with video title as filename
        'progress_hooks': [progress_hook]  # Show download progress
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

def progress_hook(d):
    if d['status'] == 'downloading':
        print(f"Downloading: {d['_percent_str']} at {d['_speed_str']}")
    elif d['status'] == 'finished':
        print(f"Download complete: {d['filename']}")

if __name__ == "__main__":
    url = input("Enter YouTube video URL: ")
    download_video(url)
