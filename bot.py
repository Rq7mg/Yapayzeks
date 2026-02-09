# bot.py
import os
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Heroku Config Vars
TOKEN = os.environ.get("TOKEN")
OPENAI_KEY = os.environ.get("OPENAI_KEY")
ALLOWED_USER_ID = int(os.environ.get("ALLOWED_USER_ID", 0))  # izinli kullanıcı ID

openai.api_key = OPENAI_KEY

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != ALLOWED_USER_ID:
        return
    await update.effective_message.reply_text(
        "Merhaba! Ben Betül’ün kölesiyim 🤖\nSadece senle konuşurum!"
    )

async def ai_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != ALLOWED_USER_ID:
        return

    user_text = update.effective_message.text
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

    await update.effective_message.reply_text(answer)

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_reply))
    print("Bot çalışıyor...")
    app.run_polling()

if __name__ == "__main__":
    main()
