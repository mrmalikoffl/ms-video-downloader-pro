from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from src.config import SUPPORTED_PLATFORMS, RATE_LIMIT_PER_HOUR

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command."""
    await update.message.reply_text(
        "📋 How to Use 🌟 Premium Video Downloader:\n"
        "1. Send a URL from YouTube, Instagram, or Twitter/X.\n"
        "2. Set quality: /quality 720p (360p, 720p, 1080p).\n"
        "3. View stats: /stats.\n"
        "4. Upgrade: /subscribe (unlimited downloads).\n"
        "5. Bot details: /bot_info.\n"
        f"📍 Platforms: {', '.join(SUPPORTED_PLATFORMS)}.\n"
        f"🆓 Free: {RATE_LIMIT_PER_HOUR} downloads/hour.\n"
        "🌟 Premium: Unlimited downloads, no waiting.\n"
        "⚠️ Only public videos. Respect platform terms.\n"
        "Admins: /admin_menu for commands."
    )

help_command = CommandHandler("help", help_command)