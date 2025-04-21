import yt_dlp
from telegram import Update
from src.downloader.progress_hook import progress_hook

def download_video(url: str, quality: str, message: Update.message, cookies_file: str = None) -> tuple:
    """Download a video."""
    ydl_opts = {
        "outtmpl": "downloads/video.%(ext)s",
        "format": f"bestvideo[height<={quality[:-1]}]+bestaudio/best[height<={quality[:-1]}]/best",
        "noplaylist": True,
        "quiet": True,
        "progress_hooks": [lambda d: progress_hook(d, message)],
    }
    # Add cookies file if provided
    if cookies_file:
        ydl_opts["cookiefile"] = cookies_file

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            return filename, None
    except Exception as e:
        return None, str(e)
