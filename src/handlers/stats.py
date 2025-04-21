from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from src.database.db_stats import get_stats
from src.database.db_premium import is_premium_user
from src.config import RATE_LIMIT_PER_HOUR

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /stats command."""
    user_id = update.message.from_user.id
    stats = get_stats(user_id)
    is_premium = is_premium_user(user_id)
    await update.message.reply_text(
        f"📊 Your Stats:\n"
        f"Total downloads: {stats['total_downloads']}\n"
        f"YouTube: {stats['youtube']}\n"
        f"Instagram: {stats['instagram']}\n"
        f"Twitter/X: {stats['twitter']}\n"
        f"Requests this hour: {stats['requests_this_hour']}/{RATE_LIMIT_PER_HOUR if not is_premium else 'Unlimited (Premium)'}"
    )

stats_command = CommandHandler("stats", stats_command)