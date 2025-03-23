import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    API_BASE_URL=os.getenv("API_BASE_URL")

    if not TELEGRAM_BOT_TOKEN:
        raise ValueError("The TELEGRAM_BOT_TOKEN environment variable is not defined in .env")
    if not API_BASE_URL:
        raise ValueError("The API_BASE_URL environment variable is not defined in .env")

config = Config()