import logging
from config.config import config
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CommandHandler
from bot.handlers import command_handlers, message_handlers

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
    
def register_handlers(application):
    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", command_handlers.start))
    application.add_handler(CommandHandler("help", command_handlers.help_command))
    
    # on non command, call the serive with the message
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handlers.echo))

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()

    # Register handlers    
    register_handlers(application)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()