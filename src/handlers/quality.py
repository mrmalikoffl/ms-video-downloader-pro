from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

async def quality_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /quality command."""
    qualities = ["360p", "720p", "1080p"]
    if not context.args:
        await update.message.reply_text(
            f"📽️ Choose a quality: {', '.join(qualities)}\nExample: /quality 720p"
        )
        return
    quality = context.args[0].lower()
    if quality not in [q.lower() for q in qualities]:
        await update.message.reply_text(
            f"❌ Invalid quality. Choose: {', '.join(qualities)}"
        )
        return
    context.user_data["quality"] = quality
    await update.message.reply_text(f"✅ Video quality set to {quality}.")

quality_command = CommandHandler("quality", quality_command)