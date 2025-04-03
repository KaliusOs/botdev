import requests
from config import TELEGRAM_CHAT_ID, BASE_URL, HUGGINGFACE_TOKEN

def send_message(chat_id, text):
    url = f"{BASE_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

def send_image_bytes(image_bytes, chat_id=None, caption=None):
    url = f"{BASE_URL}/sendPhoto"
    files = {'photo': ("image.jpg", image_bytes, "image/jpeg")}
    data = {
        "chat_id": chat_id or TELEGRAM_CHAT_ID,
    }
    if caption:
        data["caption"] = caption
    requests.post(url, data=data, files=files)

def get_chat_id(update):
    return update.get("message", {}).get("chat", {}).get("id")

def get_message_text(update):
    return update.get("message", {}).get("text", "")

def generate_image_hf(prompt):
    api_url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
    headers = {"Authorization": HUGGINGFACE_TOKEN}
    payload = {"inputs": prompt}
    response = requests.post(api_url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.content
    else:
        print("Errore HuggingFace:", response.status_code, response.text)
        return None
