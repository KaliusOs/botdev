import time
import random
import os
from functions import generate_image_hf, send_image_bytes  # <-- importa queste
# from functions import generate_images, send_photo  <-- non più necessario

def run_generation_loop(chat_id, raw_prompts, style_text):
    print("🟢 Avvio generazione immagini per Telegram")

    prompts = [p.strip() for p in raw_prompts.strip().split("\n\n") if p.strip()]
    if len(prompts) == 1:
        prompts = [p.strip() for p in raw_prompts.strip().split("\n") if p.strip()]

    state_file = f"generated_{chat_id}.txt"
    already_done = []

    if os.path.exists(state_file):
        with open(state_file, "r", encoding="utf-8") as f:
            already_done = [line.strip() for line in f.readlines() if line.strip()]

    for idx, prompt in enumerate(prompts):
        if prompt in already_done:
            print(f"⚠️ Prompt già fatto, salto {idx+1}")
            continue

        full_prompt = f"{prompt}\n{style_text}"

        try:
            print(f"\n🎨 [{idx+1}/{len(prompts)}] Generazione immagine...")
            image_bytes = generate_image_hf(full_prompt)
            if image_bytes:
                caption = f"🖼 Immagine {idx+1}/{len(prompts)}"
                send_image_bytes(image_bytes, chat_id=chat_id, caption=caption)
                print("✅ Immagine inviata.")
                with open(state_file, "a", encoding="utf-8") as f:
                    f.write(prompt + "\n\n")
            else:
                print("❌ Nessuna immagine generata.")
        except Exception as e:
            print(f"⚠️ Errore: {e}")

        sleep_time = random.randint(180, 300)
        print(f"⏳ Pausa {sleep_time // 60} min...")
        time.sleep(sleep_time)
