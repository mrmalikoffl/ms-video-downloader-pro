from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from src.config import ADMIN_IDS
from src.database.db_premium import get_premium_users_list

async def premium_users_list_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /premium_users_list command."""
    user_id = update.message.from_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("❌ You are not authorized.")
        return
    premium_users = get_premium_users_list()
    if not premium_users:
        await update.message.reply_text("📋 No premium users found.")
        return
    user_list = "\n".join([f"User ID: {u[0]}, Expires: {u[1]}" for u in premium_users])
    await update.message.reply_text(f"🌟 Premium Users List:\n{user_list}")

premium_users_list_command = CommandHandler("premium_users_list", premium_users_list_command)