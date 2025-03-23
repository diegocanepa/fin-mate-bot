import logging
from flask import Flask, request
from typing import Optional
from config.config import config
from telegram import Update, Bot
from telegram.ext import Application, MessageHandler, filters, CommandHandler
from bot.handlers import command_handlers, message_handlers
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

class TelegramWebhook(BaseModel):
    '''
    Telegram Webhook Model using Pydantic for request body validation
    '''
    update_id: int
    message: Optional[dict]
    edited_message: Optional[dict]
    channel_post: Optional[dict]
    edited_channel_post: Optional[dict]
    inline_query: Optional[dict]
    chosen_inline_result: Optional[dict]
    callback_query: Optional[dict]
    shipping_query: Optional[dict]
    pre_checkout_query: Optional[dict]
    poll: Optional[dict]
    poll_answer: Optional[dict]
    

def register_handlers(application):
    application.add_handler(CommandHandler("start", command_handlers.start))
    application.add_handler(CommandHandler("help", command_handlers.help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handlers.echo))

@app.post("/webhook")
def webhook(webhook_data: TelegramWebhook):
    '''
    Telegram Webhook
    '''
    # Method 1
    webhook_data = TelegramWebhook(**request.get_json())
    bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
    update = Update.de_json(webhook_data, bot) 
    application = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()
    register_handlers(application)

    # handle webhook request
    application.process_update(update)
    
    return {"message": "ok"}

    
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


if __name__ == '__main__':
    # Run the Flask application using Uvicorn for better performance in production.
    # Host '0.0.0.0' makes the application accessible from outside the container.
    # Port '8080' is the default port for this application.
    logger.info("Starting Flask development server...")
    app.run(host="0.0.0.0", port=8080)