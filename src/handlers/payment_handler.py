from telegram import Update
from telegram.ext import MessageHandler, filters, ContextTypes
from src.database.db_premium import grant_premium

async def handle_successful_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle successful Telegram Stars payment."""
    user_id = update.message.from_user.id
    payload = update.message.successful_payment.invoice_payload
    days = {
        "daily": 1,
        "weekly": 7,
        "monthly": 30,
        "yearly": 365,
    }.get(payload)
    if days:
        grant_premium(user_id, days)
        await update.message.reply_text(
            f"🎉 Thank you for your purchase! You're now a Premium user for {days} days.\n"
            "Enjoy unlimited downloads with no waiting period! 🚀"
        )
    else:
        await update.message.reply_text("❌ Invalid payment. Contact @YourTelegramAccount.")

handle_successful_payment = MessageHandler(filters.SUCCESSFUL_PAYMENT, handle_successful_payment)