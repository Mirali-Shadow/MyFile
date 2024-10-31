from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext

# توکن بات شما
TOKEN = "6414679474:AAHBrTFt5sCbbudkXHu3JvPrR_Pj50T30qs"

# تابع برای ارسال فایل به کاربر
async def start(update: Update, context: CallbackContext) -> None:
    await context.bot.send_document(chat_id=update.effective_chat.id, document=open("https://github.com/Mirali-Shadow/MyFile/blob/1da71e7d2321d5224725caefceb6571ccea67962/Pishro%20-%20Tamum%20Shode%20(featuring%20Kamyar).mp3", 'rb'))

# راه‌اندازی و افزودن هندلرها
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

if __name__ == "__main__":
    main()
