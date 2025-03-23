import logging
from flask import Flask
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
    bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
    update = Update.de_json(webhook_data.dict(), bot)  # Convert the Telegram Webhook class to dictionary using dict() method
    application = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()
    register_handlers(application)

    # handle webhook request
    application.process_update(update)
    
    return {"message": "ok"}

    
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
