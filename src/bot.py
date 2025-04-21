# In src/bot.py
import logging
import os
from telegram.ext import Application
from src.database.db_init import init_db
from src.handlers.start import start
from src.handlers.help import help_command
from src.handlers.quality import quality_command
from src.handlers.stats import stats_command
from src.handlers.subscribe import subscribe_command, callback_query_handler
from src.handlers.bot_info import bot_info_command
from src.handlers.url_handler import handle_url_handler
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

    # Initialize database
    try:
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise

    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()

    # Add handlers
    application.add_handler(start)  # Start command
    application.add_handler(help_command)  # Help command
    application.add_handler(quality_command)  # Quality selection
    application.add_handler(stats_command)  # User stats
    application.add_handler(subscribe_command)  # Subscription command
    application.add_handler(bot_info_command)  # Bot info
    application.add_handler(handle_url_handler)  # URL processing with auto-deletion after 5 minutes
    application.add_handler(admin_menu_command)  # Admin menu
    application.add_handler(grant_premium_command)  # Grant premium access
    application.add_handler(revoke_premium_command)  # Revoke premium access
    application.add_handler(users_list_command)  # List all users
    application.add_handler(premium_users_list_command)  # List premium users
    application.add_handler(admin_stats_command)  # Admin stats
    application.add_handler(callback_query_handler)  # Subscription callback queries
    application.add_handler(handle_successful_payment)  # Payment processing
    application.add_error_handler(error_handler)  # Error handling

    # Start the bot with explicit allowed updates for efficiency
    application.run_polling(allowed_updates=["message", "callback_query", "pre_checkout_query", "successful_payment"])

if __name__ == "__main__":
    main()
