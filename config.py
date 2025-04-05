import os

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN", "")

BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"
