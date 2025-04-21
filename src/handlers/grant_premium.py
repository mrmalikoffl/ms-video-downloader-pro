from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from src.config import ADMIN_IDS
from src.database.db_premium import grant_premium

async def grant_premium_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /grant_premium command."""
    user_id = update.message.from_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("❌ You are not authorized.")
        return
    if len(context.args) != 2:
        await update.message.reply_text(
            "Usage: /grant_premium <user_id> <days>\nExample: /grant_premium 123456789 30"
        )
        return
    try:
        target_user_id = int(context.args[0])
        days = int(context.args[1])
        if days not in [1, 7, 30, 365]:
            await update.message.reply_text("❌ Days must be 1, 7, 30, or 365.")
            return
        grant_premium(target_user_id, days)
        await update.message.reply_text(
            f"✅ Premium granted to user {target_user_id} for {days} days."
        )
    except ValueError:
        await update.message.reply_text("❌ Invalid user ID or days.")

grant_premium_command = CommandHandler("grant_premium", grant_premium_command)