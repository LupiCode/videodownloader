import os
import yt_dlp
from flask import Flask, render_template, request, jsonify, Response

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    url = request.form.get('url')
    audio_only = request.form.get('audio_only') == 'on'

    # Define the download options (simplified without postprocessor)
    ydl_opts = {
        'format': 'bestaudio/best' if audio_only else 'best',
        'progress_hooks': [progress_hook]  # Progress hook to handle updates
    }

    # Streaming response to handle the progress updates
    def generate():
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # The download process
            info_dict = ydl.extract_info(url, download=True)
            video_title = info_dict.get('title', 'video')
            yield f"Download of {video_title} started!"

    return Response(generate(), content_type='text/html;charset=utf-8')

# Hook function for progress updates
def progress_hook(d):
    if d['status'] == 'downloading':
        # You can log the downloading status or send messages here if needed
        print("Downloading...")
    elif d['status'] == 'finished':
        print("Download finished!")

if __name__ == '__main__':
    app.run(debug=True)
