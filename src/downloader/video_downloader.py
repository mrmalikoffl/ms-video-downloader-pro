# In src.downloader.video_downloader
import yt_dlp
import logging
from telegram import Update
from src.downloader.progress_hook import progress_hook

logger = logging.getLogger(__name__)

def download_video(url: str, quality: str, message: Update.message, cookies_file: str = None) -> tuple:
    """Download a video from a given URL with specified quality."""
    ydl_opts = {
        "outtmpl": f"downloads/{message.message_id}_video.%(ext)s",
        "format": f"bestvideo[height<={quality[:-1]}]+bestaudio/best[height<={quality[:-1]}]/best",
        "noplaylist": True,
        "quiet": False,
        "no_warnings": False,
        "progress_hooks": [lambda d: progress_hook(d, message)],
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }
    if cookies_file:
        ydl_opts["cookiefile"] = cookies_file

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            logger.debug(f"Successfully downloaded {url} to {filename}")
            return filename, None
    except yt_dlp.utils.DownloadError as e:
        if "ffmpeg is not installed" in str(e):
            logger.warning(f"ffmpeg not installed, falling back to single format for {url}")
            ydl_opts["format"] = "bestvideo"  # More general fallback for Instagram
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info)
                    logger.debug(f"Successfully downloaded {url} to {filename} with fallback format")
                    return filename, None
            except Exception as fallback_e:
                logger.error(f"Fallback download failed for {url}: {str(fallback_e)}")
                return None, str(fallback_e)
        logger.error(f"Download error for {url} with cookies_file={cookies_file}: {str(e)}")
        return None, str(e)
    except yt_dlp.utils.ExtractorError as e:
        logger.error(f"Extractor error for {url} with cookies_file={cookies_file}: {str(e)}")
        return None, str(e)
    except Exception as e:
        logger.error(f"Unexpected error downloading {url} with cookies_file={cookies_file}: {str(e)}")
        return None, str(e)
