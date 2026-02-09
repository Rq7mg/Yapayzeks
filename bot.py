import os
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

from transformers import pipeline

# ---------------------------
# Ayarlar
# ---------------------------
TOKEN = os.environ.get("TOKEN")
ALLOWED_USER_ID = int(os.environ.get("ALLOWED_USER_ID", "0"))

# ---------------------------
# AI pipeline (küçük model)
# ---------------------------
generator = pipeline('text-generation', model='distilgpt2')

def generate_reply(user_message: str) -> str:
    # mizahi, Betül temalı cevaplar üret
    prompt = f"Betül'ün kölesi tarzında mizahi cevap ver: {user_message}"
    result = generator(prompt, max_length=100, do_sample=True, temperature=0.8)
    text = result[0]['generated_text']
    # sadece prompt sonrası kısmı dön
    reply = text[len(prompt):].strip()
    # eğer model boş dönerse fallback
    if not reply:
        reply = random.choice([
            "Betül’ün kölesi burada! 😎",
            "Haha, bunu bekliyordun değil mi?",
            "Beni konuşturma, mizah yapacağım şimdi! 😂"
        ])
    return reply

# ---------------------------
# Komutlar
# ---------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ALLOWED_USER_ID:
        return
    await update.message.reply_text(
        "Betül’ün kölesi botu hazır! 🤖\n\n"
        "Benle sohbet edebilirsin, mizahımı göreceksin!"
    )

async def ai_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id != ALLOWED_USER_ID:
        return  # sadece izin verilen kişi
    user_text = update.message.text
    reply = generate_reply(user_text)
    await update.message.reply_text(reply)

# ---------------------------
# Main
# ---------------------------
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    
    # Komutlar
    app.add_handler(CommandHandler("start", start))
    
    # Tüm mesajları AI ile cevapla
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_chat))
    
    print("Bot çalışıyor...")
    app.run_polling()

if __name__ == "__main__":
    main()
