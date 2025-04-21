from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from src.config import SUPPORTED_PLATFORMS

async def bot_info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /bot_info command."""
    await update.message.reply_text(
        "ℹ️ About 🌟 Premium Video Downloader:\n"
        "Version: 1.0\n"
        f"Platforms: {', '.join(SUPPORTED_PLATFORMS)}\n"
        "Features: Video downloads, quality selection, premium subscriptions\n"
        "Contact: Send payment screenshots or queries to @YourTelegramAccount\n"
        "⚠️ Respect platform terms and copyright laws."
    )

bot_info_command = CommandHandler("bot_info", bot_info_command)