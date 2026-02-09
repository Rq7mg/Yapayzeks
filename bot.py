# bot.py
import os
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("TOKEN")  # Heroku Config Var olarak ekle
OPENAI_KEY = os.environ.get("OPENAI_KEY")  # Heroku Config Var olarak ekle
ALLOWED_USER_ID = int(os.environ.get("ALLOWED_USER_ID", 0))  # İzinli Telegram ID

openai.api_key = OPENAI_KEY

# ----------------- /start -----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ALLOWED_USER_ID:
        return
    await update.message.reply_text(
        "Merhaba! Ben Betül’ün kölesiyim 🤖\nSadece senle konuşurum ve mizahımı bolca paylaşırım!"
    )

# ----------------- AI cevap -----------------
async def ai_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ALLOWED_USER_ID:
        return

    user_text = update.message.text
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_text}],
            max_tokens=150,
            temperature=0.9
        )
        answer = response['choices'][0]['message']['content']
    except Exception as e:
        answer = "Üzgünüm, bir hata oluştu 🤖"

    await update.message.reply_text(answer)

# ----------------- Main -----------------
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_reply))
    print("Bot çalışıyor...")
    app.run_polling()

if __name__ == "__main__":
    main()
