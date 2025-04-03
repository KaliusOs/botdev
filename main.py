from flask import Flask, request
from functions import send_message, get_chat_id, get_message_text
from threading import Thread
from image_scheduler import run_generation_loop

app = Flask(__name__)
user_sessions = {}

@app.route("/", methods=["GET"])
def home():
    return "Bot attivo", 200

@app.route("/", methods=["POST"])
def webhook():
    update = request.get_json()
    print("Update ricevuto:", update)

    chat_id = get_chat_id(update)
    message = get_message_text(update).strip()

    if not chat_id or not message:
        return "OK", 200

    if message == "/start":
        send_message(chat_id, "Benvenuto! Inviami una descrizione e genererò delle immagini artistiche per te.")
    
    elif message == "/startauto":
        user_sessions[chat_id] = {"step": "awaiting_prompts"}
        send_message(chat_id, "🧾 Inviami ora la **lista di descrizioni**, una dopo l’altra (puoi copiarle tutte insieme).")

    elif chat_id in user_sessions:
        session = user_sessions[chat_id]

        if session["step"] == "awaiting_prompts":
            session["prompts"] = message
            session["step"] = "awaiting_style"
            send_message(chat_id, "🎨 Perfetto! Ora inviami lo **stile artistico da applicare**.")

        elif session["step"] == "awaiting_style":
            session["style"] = message
            send_message(chat_id, "⏳ Avvio della generazione automatica delle immagini...")
            Thread(target=run_generation_loop, args=(chat_id, session["prompts"], session["style"])).start()
            del user_sessions[chat_id]

    return "OK", 200

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
