import logging
from flask import Flask, request, jsonify
from telegram import Update
from config.config import config
from telegram.ext import Application, MessageHandler, filters, CommandHandler
from bot.handlers import command_handlers, message_handlers

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Initialize Telegram Bot Application (without running polling)
telegram_app = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()

@app.route('/api/webhook', methods=['POST'])
async def webhook():
    """Handles incoming webhook requests from Telegram."""
    try:
        data = request.get_json(force=True)
        update = Update.de_json(data, telegram_app.bot)
        await telegram_app.process_update(update)
        return jsonify({"status": "OK"}), 200
    except Exception as e:
        logger.error(f"Error processing webhook: {e}", exc_info=True)
        return jsonify({"status": "Error", "message": str(e)}), 500

@app.route('/set_webhook', methods=['GET'])
async def set_webhook():
    """Sets the Telegram webhook URL. This should be called once after deployment."""
    vercel_url = request.headers.get('x-vercel-deployment-url')
    if not vercel_url:
        return jsonify({"status": "Error", "message": "Vercel URL not found in headers."}), 400

    webhook_url = f"https://{vercel_url}/api/webhook"
    try:
        webhook_info = await telegram_app.bot.set_webhook(webhook_url)
        return jsonify({"status": "Webhook set", "webhook_info": webhook_info}), 200
    except Exception as e:
        logger.error(f"Error setting webhook: {e}", exc_info=True)
        return jsonify({"status": "Error", "message": str(e)}), 500

@app.route('/')
def hello():
    """Simple health check endpoint."""
    return "FinMate Bot is running (Webhook Mode)"


def register_handlers(telegram_app):
    # on different commands - answer in Telegram
    telegram_app.add_handler(CommandHandler("start", command_handlers.start))
    telegram_app.add_handler(CommandHandler("help", command_handlers.help_command))
    
    # on non command, call the serive with the message
    telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handlers.echo))
    
async def initialize_telegram_app():
    """Initializes the Telegram Application."""
    register_handlers(telegram_app)
    await telegram_app.initialize()  # Explicitly initialize
    return telegram_app

if __name__ == '__main__':
    # This should not be run in Vercel. Vercel will handle requests to /api/webhook
    import asyncio
    asyncio.run(initialize_telegram_app()) 
    app.run(debug=True, port=8080)