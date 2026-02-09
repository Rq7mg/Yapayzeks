import os
from collections import deque
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# ----------------------------
# AYARLAR
# ----------------------------
TOKEN = os.environ.get("TOKEN")  # Telegram bot token
OPENAI_KEY = os.environ.get("OPENAI_KEY")  # OpenAI API key
ALLOWED_USER_ID = int(os.environ.get("ALLOWED_USER_ID", "0"))  # Cevap verilecek Telegram ID
MEMORY_SIZE = 10  # Son mesaj sayısı, AI context için

openai.api_key = OPENAI_KEY
conversation_history = deque(maxlen=MEMORY_SIZE)

# ----------------------------
# START KOMUTU
# ----------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ALLOWED_USER_ID:
        await update.message.reply_text("🚫 Sen Betül’ün kölesi değilsin, giremezsin!")
        return

    await update.message.reply_text(
        "✨ Selam! Ben Betül’ün mizah dolu kölesi! 🤖\n"
        "🗨️ Bana mesaj at, seninle konuşurum ve Betül temalı espriler yaparım.\n"
        "⚡ AI desteğim var, aklını karıştıracak kadar zeki ve eğlenceliyim!\n\n"
        "Hadi mesajını yaz, başlıyoruz!"
    )

# ----------------------------
# AI YANIT HANDLER
# ----------------------------
async def ai_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id != ALLOWED_USER_ID:
        return  # sadece izinli kullanıcıya yanıt ver

    user_message = update.message.text
    conversation_history.append({"role": "user", "content": user_message})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": (
                    "Sen Betül’ün mizah dolu kölesisin, esprili, eğlenceli ve zeki cevaplar veriyorsun. "
                    "Mesajlara her zaman mizah kat, Betül’ün temasıyla bağla."
                )}
            ] + list(conversation_history)
        )
        reply_text = response.choices[0].message.content.strip()
        conversation_history.append({"role": "assistant", "content": reply_text})
        await update.message.reply_text(reply_text)
    except Exception as e:
        await update.message.reply_text(f"⚠️ Hata: {e}")

# ----------------------------
# BOT BAŞLATMA
# ----------------------------
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_reply))
    print("🤖 Betül’ün mizah dolu AI botu çalışıyor...")
    app.run_polling()

if __name__ == "__main__":
    main()
