from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from src.config import ADMIN_IDS
from src.database.db_premium import revoke_premium

async def revoke_premium_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /revoke_premium command."""
    user_id = update.message.from_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("❌ You are not authorized.")
        return
    if len(context.args) != 1:
        await update.message.reply_text(
            "Usage: /revoke_premium <user_id>\nExample: /revoke_premium 123456789"
        )
        return
    try:
        target_user_id = int(context.args[0])
        revoke_premium(target_user_id)
        await update.message.reply_text(
            f"✅ Premium revoked for user {target_user_id}."
        )
    except ValueError:
        await update.message.reply_text("❌ Invalid user ID.")

revoke_premium_command = CommandHandler("revoke_premium", revoke_premium_command)