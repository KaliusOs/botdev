
from flask import Flask, request
from functions import send_message, send_photo, generate_images

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Bot attivo", 200

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    message = data.get("message", {}).get("text", "")
    chat_id = data.get("message", {}).get("chat", {}).get("id", "")

    if message:
        send_message("Sto generando le immagini…")
        images = generate_images(message)
        for img_url in images:
            send_photo(img_url)

    return "ok", 200

if __name__ == "__main__":
    app.run()
