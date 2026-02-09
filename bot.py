import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI

# -------------------------------
# Ayarlar
# -------------------------------
TOKEN = os.environ.get("TELEGRAM_TOKEN")  # Heroku Config Var
TARGET_ID = int(os.environ.get("TARGET_ID"))  # AI'nin cevap vereceği kullanıcı/ID
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

# -------------------------------
# Komutlar
# -------------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Selam! Betül’ün kölesi olarak buradayım 😎\n"
        "Bana mesaj at, sana AI cevaplar üreteyim!"
    )

# -------------------------------
# Mesaj işleme
# -------------------------------
async def ai_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Sadece belirlenen TARGET_ID'ye cevap verir
    if update.message.from_user.id != TARGET_ID:
        return

    user_text = update.message.text

    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=user_text
        )
        ai_text = response.output_text
        await update.message.reply_text(ai_text)

    except Exception as e:
        await update.message.reply_text(f"⚠️ AI cevap verirken hata: {e}")

# -------------------------------
# Bot başlatma
# -------------------------------
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_reply))

    print("🤖 AI Telegram bot çalışıyor...")
    app.run_polling()

if __name__ == "__main__":
    main()
