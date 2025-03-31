import requests
import openai
from config import BASE_URL, TELEGRAM_CHAT_ID, OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def send_message(text):
    url = f"{BASE_URL}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
    requests.post(url, json=payload)

def send_photo(photo_url):
    url = f"{BASE_URL}/sendPhoto"
    data = {"chat_id": TELEGRAM_CHAT_ID, "photo": photo_url}
    requests.post(url, data=data)

def generate_images(prompt):
    full_prompt = f"""
{prompt}
Style artistique : Aquarelle + encre, Contrasté, textures granuleuses,
Palette : noir, brun, rouge, beige poussière,
Typographie dessinée à la main ou effet pinceau / gratté,
Format portrait vertical 1080x1920 px format 9:16 (TikTok).
Ne pas inclure de texte sur l'image.
"""
    images = []
    for _ in range(10):
        response = openai.Image.create(
            prompt=full_prompt,
            n=1,
            size="1024x1792",
            model="dall-e-3"
        )
        image_url = response["data"][0]["url"]
        images.append(image_url)
    return images
