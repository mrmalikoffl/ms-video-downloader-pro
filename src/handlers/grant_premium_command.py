import logging
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from src.config import ADMIN_IDS
from src.database.db_premium import grant_premium

logger = logging.getLogger(__name__)

async def grant_premium_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /grant_premium command with admin and user notifications."""
    admin_id = update.message.from_user.id
    if admin_id not in ADMIN_IDS:
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

        # Grant premium and get expiry date
        expiry_date = grant_premium(target_user_id, days)

        # Notify admin
        admin_message = (
            f"✅ Premium granted to user {target_user_id}\n"
            f"📅 Plan: {days} days\n"
            f"⏰ Expires: {expiry_date}"
        )
        await update.message.reply_text(admin_message)

        # Notify user
        user_message = (
            f"🎉 You have been granted premium status!\n"
            f"🆔 User ID: {target_user_id}\n"
            f"📅 Plan: {days} days\n"
            f"⏰ Expires: {expiry_date}"
        )
        try:
            await context.bot.send_message(chat_id=target_user_id, text=user_message)
        except Exception as e:
            logger.error(f"Failed to notify user {target_user_id}: {str(e)}")
            await update.message.reply_text(
                f"⚠️ Premium granted, but failed to notify user {target_user_id}: {str(e)}"
            )

    except ValueError:
        await update.message.reply_text("❌ Invalid user ID or days.")
    except Exception as e:
        logger.error(f"Error granting premium: {str(e)}")
        await update.message.reply_text(f"❌ Failed to grant premium: {str(e)}")

grant_premium_handler = CommandHandler("grant_premium", grant_premium_command)
