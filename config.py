import os

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

if not all([TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, OPENAI_API_KEY, HUGGINGFACE_TOKEN]):
    raise ValueError("Una o più variabili d'ambiente non sono state impostate correttamente.")

BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"
