from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from src.database.db_premium import is_premium_user

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command."""
    user_id = update.message.from_user.id
    is_premium = is_premium_user(user_id)
    welcome_text = (
        "🎥 Welcome to 🌟 Premium Video Downloader 🌟!\n"
        "Download videos from YouTube, Instagram, and Twitter/X with ease.\n\n"
        "✨ Features:\n"
        "- 📹 Multi-platform support\n"
        "- 🎨 Choose quality (360p, 720p, 1080p)\n"
        "- ⏳ Real-time progress updates\n"
        "- 📊 Usage stats (/stats)\n"
        "- 🌟 Premium: Unlimited downloads (/subscribe)\n"
        "- ℹ️ Bot info (/bot_info)\n\n"
        f"{'🚀 You’re a Premium user! Unlimited downloads!' if is_premium else '🆓 Free user: 5 downloads/hour. Upgrade with /subscribe.'}\n"
        "⚠️ Respect platform terms and copyright laws.\n"
        "Use /help for instructions."
    )
    await update.message.reply_text(welcome_text)

start = CommandHandler("start", start)