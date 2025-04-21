import logging
import os
from telegram.ext import Application, ContextTypes
from src.handlers.start import start
from src.handlers.help import help_command
from src.handlers.quality import quality_command
from src.handlers.stats import stats_command
from src.handlers.subscribe import subscribe_command, callback_query_handler
from src.handlers.bot_info import bot_info_command
from src.handlers.url_handler import handle_url
from src.handlers.admin_menu import admin_menu_command
from src.handlers.grant_premium import grant_premium_command
from src.handlers.revoke_premium import revoke_premium_command
from src.handlers.users_list import users_list_command
from src.handlers.premium_users_list import premium_users_list_command
from src.handlers.admin_stats import admin_stats_command
from src.handlers.payment_handler import handle_successful_payment
from src.handlers.error_handler import error_handler

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot token
BOT_TOKEN = os.getenv("BOT_TOKEN")

def main():
    """Run the bot."""
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN environment variable not set.")

    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()

    # Add handlers
    application.add_handler(start)
    application.add_handler(help_command)
    application.add_handler(quality_command)
    application.add_handler(stats_command)
    application.add_handler(subscribe_command)
    application.add_handler(bot_info_command)
    application.add_handler(handle_url)
    application.add_handler(admin_menu_command)
    application.add_handler(grant_premium_command)
    application.add_handler(revoke_premium_command)
    application.add_handler(users_list_command)
    application.add_handler(premium_users_list_command)
    application.add_handler(admin_stats_command)
    application.add_handler(callback_query_handler)
    application.add_handler(handle_successful_payment)
    application.add_error_handler(error_handler)

    # Start the bot
    application.run_polling(allowed_updates=ContextTypes.DEFAULT_TYPE.ALL_TYPES)

if __name__ == "__main__":
    main()