# In src.handlers.url_handler
import logging
from telegram import Update
from telegram.ext import MessageHandler, filters, ContextTypes
from src.utils.url_validator import is_valid_url
from src.utils.file_cleanup import cleanup_file
from src.database.db_requests import record_request
from src.database.db_premium import is_premium_user
from src.database.db_requests import check_rate_limit
from src.downloader.video_downloader import download_video
from src.config import SUPPORTED_PLATFORMS, RATE_LIMIT_PER_HOUR, ADMIN_IDS

logger = logging.getLogger(__name__)

async def delete_video_message(context: ContextTypes.DEFAULT_TYPE):
    """Callback to delete the video message, success message, and guide message from the chat."""
    job = context.job
    chat_id = job.data["chat_id"]
    video_message_id = job.data["video_message_id"]
    success_message_id = job.data["success_message_id"]
    guide_message_id = job.data["guide_message_id"]
    filename = job.data.get("filename")

    # Delete video message
    try:
        await context.bot.delete_message(chat_id=chat_id, message_id=video_message_id)
        logger.debug(f"Deleted video message {video_message_id} from chat {chat_id}")
    except Exception as e:
        logger.error(f"Failed to delete video message {video_message_id} from chat {chat_id}: {str(e)}")

    # Delete success message
    try:
        await context.bot.delete_message(chat_id=chat_id, message_id=success_message_id)
        logger.debug(f"Deleted success message {success_message_id} from chat {chat_id}")
    except Exception as e:
        logger.error(f"Failed to delete success message {success_message_id} from chat {chat_id}: {str(e)}")

    # Delete guide message
    try:
        await context.bot.delete_message(chat_id=chat_id, message_id=guide_message_id)
        logger.debug(f"Deleted guide message {guide_message_id} from chat {chat_id}")
    except Exception as e:
        logger.error(f"Failed to delete guide message {guide_message_id} from chat {chat_id}: {str(e)}")

    # Clean up local file
    if filename:
        try:
            cleanup_file(filename)
            logger.debug(f"Cleaned up file: {filename}")
        except Exception as e:
            logger.error(f"Failed to clean up file {filename}: {str(e)}")

async def handle_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming URLs."""
    user_id = update.message.from_user.id
    url = update.message.text.strip()

    # Check rate limit for non-premium users
    is_premium = is_premium_user(user_id)
    if user_id not in ADMIN_IDS and not is_premium:
        if not check_rate_limit(user_id):
            await update.message.reply_text(
                f"🚫 You've reached the hourly limit of {RATE_LIMIT_PER_HOUR} downloads. "
                "Upgrade with /subscribe for unlimited downloads! 🌟"
            )
            return

    if not is_valid_url(url):
        await update.message.reply_text(
            f"❌ Please send a valid URL from {', '.join(SUPPORTED_PLATFORMS)}."
        )
        return

    # Record request
    platform = next((p for p in SUPPORTED_PLATFORMS if p.lower() in url.lower()), "unknown")
    record_request(user_id, platform)

    # Send processing message and store it
    processing_message = await update.message.reply_text("⏳ Processing your video... Please wait.")

    # Get quality
    quality = context.user_data.get("quality", "720p")

    # Define cookies file path
    cookies_file = None
    if "instagram" in platform.lower():
        cookies_file = "/app/src/cookies/instagram_cookies.txt"
    elif "youtube" in platform.lower():
        cookies_file = "/app/src/cookies/youtube_cookies.txt"

    # Download video
    filename, error = download_video(url, quality, update.message, cookies_file=cookies_file)

    if error:
        if "sign in to confirm" in error.lower():
            await update.message.reply_text(
                "❌ YouTube requires additional verification for this video. Try another video or contact support."
            )
        else:
            await update.message.reply_text(f"❌ Oops! Something went wrong: {error}")
        return

    # Send video, delete processing message, send guide, and schedule deletion
    try:
        with open(filename, "rb") as video_file:
            video_message = await update.message.reply_video(video=video_file)
        success_message = await update.message.reply_text("✅ Video downloaded successfully! 🎉")
        guide_message = await update.message.reply_text(
            "📥 **Download Guide**  \n"
            "To save the above video to your gallery:  \n"
            "1. Click the three dots (⋮) on the video's right corner.  \n"
            "2. Select **Save to Downloads** or **Save to Gallery**.  \n"
            "Thank you! 😊",
            parse_mode="Markdown"
        )

        # Delete the processing message
        try:
            await context.bot.delete_message(
                chat_id=processing_message.chat_id,
                message_id=processing_message.message_id
            )
            logger.debug(f"Deleted processing message {processing_message.message_id} from chat {processing_message.chat_id}")
        except Exception as e:
            logger.error(f"Failed to delete processing message {processing_message.message_id}: {str(e)}")

        # Schedule video, success, and guide message deletion after 5 minutes (300 seconds)
        context.job_queue.run_once(
            callback=delete_video_message,
            when=300,
            data={
                "chat_id": update.message.chat_id,
                "video_message_id": video_message.message_id,
                "success_message_id": success_message.message_id,
                "guide_message_id": guide_message.message_id,
                "filename": filename
            },
            name=f"delete_video_{video_message.message_id}"
        )
        logger.debug(f"Scheduled deletion of video message {video_message.message_id}, success message {success_message.message_id}, and guide message {guide_message.message_id} in 5 minutes")
    except Exception as e:
        await update.message.reply_text(f"❌ Failed to send video: {str(e)}")
        if filename:
            try:
                cleanup_file(filename)
                logger.debug(f"Cleaned up file: {filename}")
            except Exception as e:
                logger.error(f"Failed to clean up file {filename}: {str(e)}")

# Define the MessageHandler
handle_url_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_url)
