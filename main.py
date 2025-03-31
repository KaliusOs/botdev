import openai
import requests
import time
import os
import schedule
from dotenv import load_dotenv
from flask import Flask, request

load_dotenv()

# === API KEYS ===
openai.api_key = os.getenv("OPENAI_API_KEY")
telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")

# === SERVER WEB PER WEBHOOK ===
app = Flask(__name__)
user_prompt = None

@app.route("/", methods=["POST"])
def webhook():
    global user_prompt
    data = request.get_json()
    message = data.get("message", {}).get("text", "")
    chat_id = data.get("message", {}).get("chat", {}).get("id", "")
    if str(chat_id) == telegram_chat_id and message:
        user_prompt = message
        send_message("Sto creando le tue immagini… ✨")
        genera_e_invia(user_prompt)
    return "OK", 200

# === FUNZIONI ===
def send_message(text):
    url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
    payload = {"chat_id": telegram_chat_id, "text": text}
    requests.post(url, json=payload)

def send_photo(url):
    requests.post(
        f"https://api.telegram.org/bot{telegram_bot_token}/sendPhoto",
        data={
            "chat_id": telegram_chat_id,
            "photo": url
        })

def genera_e_invia(prompt_user):
    prompt = f"""
{prompt_user}
Style artistique : Aquarelle + encre, Contrasté, textures granuleuses,
Palette : noir, brun, rouge, beige poussière,
Typographie dessinée à la main ou effet pinceau / gratté,
Format portrait vertical 1080x1920 px format 9:16 (TikTok).
Ne pas inclure de texte sur l'image.
"""
    for i in range(10):
        try:
            client = openai.OpenAI()
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1792",
                n=1
            )
            img_url = response.data[0].url
            send_photo(img_url)
            time.sleep(2)
        except Exception as e:
            send_message(f"Errore durante la generazione: {e}")

# === MESSAGGIO GIORNALIERO ===
def messaggio_giornaliero():
    send_message(
        "Buongiorno! 😄 Inviami una descrizione e creerò delle immagini artistiche per te."
    )

# === SCHEDULAZIONE ===
schedule.every().day.at("09:00").do(messaggio_giornaliero)

def scheduler_loop():
    while True:
        schedule.run_pending()
        time.sleep(1)

# === AVVIO ===
if __name__ == "__main__":
    from threading import Thread
    Thread(target=scheduler_loop).start()
    app.run(host="0.0.0.0", port=8080)
