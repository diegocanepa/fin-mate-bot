import logging
from flask import Flask
from typing import Optional
from config.config import config
from telegram import Update, Bot
from telegram.ext import Dispatcher, MessageHandler, filters, CommandHandler
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
    

def register_handlers(dispatcher):
    dispatcher.add_handler(CommandHandler("start", command_handlers.start))
    dispatcher.add_handler(CommandHandler("help", command_handlers.help_command))
    dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handlers.echo))

@app.post("/webhook")
def webhook(webhook_data: TelegramWebhook):
    '''
    Telegram Webhook
    '''
    # Method 1
    bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
    update = Update.de_json(webhook_data.__dict__, bot) # convert the Telegram Webhook class to dictionary using __dict__ dunder method
    dispatcher = Dispatcher(bot, None, workers=4)
    register_handlers(dispatcher)

    # handle webhook request
    dispatcher.process_update(update)
    
    return {"message": "ok"}

    
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"