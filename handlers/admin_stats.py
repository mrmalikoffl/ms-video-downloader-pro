from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from src.config import ADMIN_IDS
from src.database.db_stats import get_stats

async def admin_stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /admin_stats command."""
    user_id = update.message.from_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("❌ You are not authorized.")
        return
    stats = get_stats(None)
    await update.message.reply_text(
        f"📈 Bot-Wide Stats:\n"
        f"Total downloads: {stats['total_downloads']}\n"
        f"YouTube: {stats['youtube']}\n"
        f"Instagram: {stats['instagram']}\n"
        f"Twitter/X: {stats['twitter']}\n"
        f"Premium users: {stats['premium_users']}"
    )

admin_stats_command = CommandHandler("admin_stats", admin_stats_command)