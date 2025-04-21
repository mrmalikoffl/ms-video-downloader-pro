from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from src.config import ADMIN_IDS
from src.database.db_stats import get_users_list

async def users_list_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /users_list command."""
    user_id = update.message.from_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("❌ You are not authorized.")
        return
    users = get_users_list()
    if not users:
        await update.message.reply_text("📋 No users found.")
        return
    user_list = "\n".join([f"User ID: {u}" for u in users])
    await update.message.reply_text(f"📋 Users List:\n{user_list}")

users_list_command = CommandHandler("users_list", users_list_command)