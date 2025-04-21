from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler, ContextTypes
from src.payments.stars_payment import send_stars_invoice
from src.payments.upi_payment import send_upi_instructions
from src.config import SUBSCRIPTION_PRICES

async def subscribe_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /subscribe command."""
    keyboard = [
        [
            InlineKeyboardButton("Pay with Telegram Stars 💸", callback_data="pay_stars"),
            InlineKeyboardButton("Pay with UPI 🇮🇳", callback_data="pay_upi"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🌟 Choose a Premium Subscription Method:\n"
        "Unlock unlimited downloads and no waiting period!\n"
        "Plans:\n"
        "- Daily: 100 Stars / $1 / ₹85\n"
        "- Weekly: 250 Stars / $2.50 / ₹210\n"
        "- Monthly: 500 Stars / $5 / ₹420\n"
        "- Yearly: 1000 Stars / $10 / ₹840"
    , reply_markup=reply_markup)

async def callback_query_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle subscription button clicks."""
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    data = query.data
    if data == "pay_stars":
        keyboard = [
            [
                InlineKeyboardButton("Daily (100 Stars)", callback_data="stars_daily"),
                InlineKeyboardButton("Weekly (250 Stars)", callback_data="stars_weekly"),
            ],
            [
                InlineKeyboardButton("Monthly (500 Stars)", callback_data="stars_monthly"),
                InlineKeyboardButton("Yearly (1000 Stars)", callback_data="stars_yearly"),
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(
            "💸 Select a Telegram Stars Plan:", reply_markup=reply_markup
        )
    elif data == "pay_upi":
        keyboard = [
            [
                InlineKeyboardButton("Daily ($1 / ₹85)", callback_data="upi_daily"),
                InlineKeyboardButton("Weekly ($2.50 / ₹210)", callback_data="upi_weekly"),
            ],
            [
                InlineKeyboardButton("Monthly ($5 / ₹420)", callback_data="upi_monthly"),
                InlineKeyboardButton("Yearly ($10 / ₹840)", callback_data="upi_yearly"),
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(
            "🇮🇳 Select a UPI Plan:", reply_markup=reply_markup
        )
    elif data.startswith("stars_"):
        plan = data.replace("stars_", "")
        if plan in SUBSCRIPTION_PRICES:
            days, stars = SUBSCRIPTION_PRICES[plan]["days"], SUBSCRIPTION_PRICES[plan]["stars"]
            await send_stars_invoice(
                context.bot,
                user_id,
                f"{plan.capitalize()} Premium Subscription",
                f"{days}-day unlimited downloads",
                plan,
                stars,
            )
    elif data.startswith("upi_"):
        plan = data.replace("upi_", "")
        if plan in SUBSCRIPTION_PRICES:
            days, usd, inr = (
                SUBSCRIPTION_PRICES[plan]["days"],
                SUBSCRIPTION_PRICES[plan]["price_usd"],
                SUBSCRIPTION_PRICES[plan]["price_inr"],
            )
            await send_upi_instructions(
                context.bot,
                user_id,
                plan,
                days,
                usd,
                inr,
            )

subscribe_command = CommandHandler("subscribe", subscribe_command)
callback_query_handler = CallbackQueryHandler(callback_query_handler)