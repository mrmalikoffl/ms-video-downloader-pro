from telegram import Update
from telegram.ext import MessageHandler, filters, ContextTypes
from src.utils.url_validator import is_valid_url
from src.utils.file_cleanup import cleanup_file
from src.database.db_requests import record_request
from src.database.db_premium import is_premium_user
from src.database.db_requests import check_rate_limit
from src.downloader.video_downloader import download_video
from src.config import SUPPORTED_PLATFORMS, RATE_LIMIT_PER_HOUR, ADMIN_IDS

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

    await update.message.reply_text("⏳ Processing your video... Please wait.")

    # Get quality
    quality = context.user_data.get("quality", "720p")

    # Download video
    filename, error = download_video(url, quality, update.message)

    if error:
        await update.message.reply_text(f"❌ Oops! Something went wrong: {error}")
        return

    # Send video
    try:
        with open(filename, "rb") as video_file:
            await update.message.reply_video(video=video_file)
        await update.message.reply_text("✅ Video downloaded successfully! 🎉")
    except Exception as e:
        await update.message.reply_text(f"❌ Failed to send video: {str(e)}")
    finally:
        cleanup_file(filename)

handle_url = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_url)