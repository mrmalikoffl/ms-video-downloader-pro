from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from src.config import ADMIN_IDS

async def admin_menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /admin_menu command."""
    user_id = update.message.from_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("❌ You are not authorized.")
        return
    await update.message.reply_text(
        "🛠️ Admin Menu:\n"
        "- /grant_premium <user_id> <days> - Grant premium (1, 7, 30, 365)\n"
        "- /revoke_premium <user_id> - Revoke premium\n"
        "- /users_list - List all users\n"
        "- /premium_users_list - List premium users\n"
        "- /admin_stats - Bot-wide stats"
    )

admin_menu_command = CommandHandler("admin_menu", admin_menu_command)