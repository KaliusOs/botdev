import requests
from config import TELEGRAM_CHAT_ID, BASE_URL
import os

HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

def generate_image_hf(prompt):
    api_url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_TOKEN}"}
    payload = {"inputs": prompt}

    response = requests.post(api_url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.content
    else:
        print("Errore HuggingFace:", response.status_code, response.text)
        return None

def send_image_bytes(image_bytes, chat_id=None, caption=None):
    url = f"{BASE_URL}/sendPhoto"
    files = {'photo': ("image.jpg", image_bytes, "image/jpeg")}
    data = {
        "chat_id": chat_id or TELEGRAM_CHAT_ID,
    }
    if caption:
        data["caption"] = caption
    requests.post(url, data=data, files=files)
