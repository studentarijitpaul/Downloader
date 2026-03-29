import yt_dlp

def download_videos(url):
    ydl_opts = {
        'format': 'bestvideo[height<=1080]',
        'merge_output_format': 'mp4',
        'outtmpl': '%(title)s.%(ext)s'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        print("Error:", e)


video_url = input("Enter YouTube URL: ")
download_videos(video_url)