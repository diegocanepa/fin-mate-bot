import logging
import httpx
from telegram import Update
from telegram.ext import ContextTypes
from config.config import config

logger = logging.getLogger(__name__)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echoes the user's message by making an HTTP request."""
    user_message = update.message.text
    logger.info(f"Received message from user {update.effective_user.id}: {user_message}")

    try:
        async with httpx.AsyncClient() as client:
            # Replace the following URL with the URL of your HTTP service
            base_api_url = config.API_BASE_URL
            headers = {'Content-Type': 'application/json'}
            response = await client.post(f'{base_api_url}/action', json={'content': user_message}, headers=headers)
            data = response.json()
            print(f'api response: {data}')
            response_text = f"API Response: {data}"
            await update.message.reply_text(response_text)
    except httpx.RequestError as e:
        logger.error(f"HTTP connection error: {e}")
        await update.message.reply_text("There was an error contacting the external service.")
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP status error {e.response.status_code}: {e.response.text}")
        await update.message.reply_text(f"The external service responded with an error: {e.response.status_code}")
    except Exception as e:
        logger.error(f"Unexpected error processing the message: {e}")
        await update.message.reply_text("An unexpected error occurred.")
