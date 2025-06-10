#!/usr/bin/env python
import logging
import os
import time

from dotenv import load_dotenv
from openai import OpenAI
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# Load environment variables from .env file in development
load_dotenv()

# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Environment variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENROUTER_KEY = os.getenv("OPENROUTER_KEY")
RAILWAY_ENV = os.getenv("RAILWAY_ENV", "development")

# Constants
FALLBACK_MESSAGE = "🧘‍♂️ Мудрец молчит…"
SYSTEM_PROMPT = (
    "You are a witty sage who provides concise, slightly ironic "
    "philosophical responses. Keep your answers short, wise, and with a "
    "touch of humor. Never be verbose."
)
RATE_LIMIT_SECONDS = 2
MAX_TOKENS = 60

# In-memory rate limiting
user_last_request = {}


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle incoming text messages."""
    # Extract user ID and message text
    user_id = update.message.from_user.id
    message_text = update.message.text

    # Apply rate limiting
    current_time = time.time()
    if user_id in user_last_request:
        time_since_last = current_time - user_last_request[user_id]
        if time_since_last < RATE_LIMIT_SECONDS:
            logger.info(f"Rate limit applied for user {user_id}")
            return

    # Update last request time
    user_last_request[user_id] = current_time

    try:
        # Create OpenAI client with OpenRouter base URL
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=OPENROUTER_KEY,
        )

        # Send request to OpenRouter (claude-3-haiku)
        response = client.chat.completions.create(
            model="anthropic/claude-3-haiku",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message_text},
            ],
            max_tokens=MAX_TOKENS,
        )

        # Extract the response
        sage_response = response.choices[0].message.content.strip()

        # Send response back to user
        await update.message.reply_text(sage_response)
        logger.info(f"Response sent to user {user_id}")

    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text(FALLBACK_MESSAGE)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text(
        "Привет! Я мудрец, который даст тебе философский совет. "
        "Просто напиши свой вопрос."
    )


def main():
    """Start the bot."""
    # Validate environment variables
    if not TELEGRAM_TOKEN:
        logger.error("TELEGRAM_TOKEN is not set")
        return
    if not OPENROUTER_KEY:
        logger.error("OPENROUTER_KEY is not set")
        return

    # Create the Application
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    # Start the Bot
    if RAILWAY_ENV == "production":
        # Use webhook in production (Railway)
        port = int(os.getenv("PORT", "8080"))
        webhook_url = os.getenv("WEBHOOK_URL")
        if webhook_url:
            application.run_webhook(
                listen="0.0.0.0",
                port=port,
                webhook_url=webhook_url,
            )
        else:
            logger.warning("WEBHOOK_URL not set, falling back to polling")
            application.run_polling()
    else:
        # Use polling in development
        application.run_polling()

    logger.info("Bot started")


if __name__ == "__main__":
    main()
