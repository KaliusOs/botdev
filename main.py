from flask import Flask, request
from functions import send_message, get_chat_id, get_message_text

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Bot attivo", 200

@app.route("/", methods=["POST"])
def webhook():
    update = request.get_json()
    chat_id = get_chat_id(update)
    message = get_message_text(update)

    if chat_id and message:
        if message == "/start":
            send_message(chat_id, "Benvenuto! Inviami una descrizione e genererò delle immagini artistiche per te.")
        else:
            send_message(chat_id, f"Hai scritto: {message}")

    return "OK", 200

# ✅ AVVIO SERVER Flask, richiesto da Render
import os
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
