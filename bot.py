from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext

# توکن بات شما
TOKEN = "6414679474:AAHBrTFt5sCbbudkXHu3JvPrR_Pj50T30qs"

# تابع برای ارسال فایل به کاربر
async def start(update: Update, context: CallbackContext) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id, text="سلام! برای دریافت فایل، لینک مخصوص را ارسال کنید.")

# تابع برای مدیریت دستور استارت خاص
async def get_file_2(update: Update, context: CallbackContext) -> None:
    print("در حال ارسال فایل از لینک getfile2...")
    try:
        await context.bot.send_document(chat_id=update.effective_chat.id,
                                         document=open("/workspaces/MyFile/Seft (Djsajjad1 & BLH Remix).mp3", 'rb'))  # مسیر فایل
        print("فایل دوم ارسال شد.")
    except Exception as e:
        print(f"خطا در ارسال فایل: {e}")
        await context.bot.send_message(chat_id=update.effective_chat.id, text="متاسفانه ارسال فایل دوم ناموفق بود.")

# تابع برای مدیریت پیام‌ها
async def handle_message(update: Update, context: CallbackContext) -> None:
    print(f"متن دریافتی: {update.message.text}")

# راه‌اندازی و افزودن هندلرها
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))  # هندلر برای /start
    app.add_handler(CommandHandler("getfile2", get_file_2))  # هندلر برای لینک getfile2
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))  # مدیریت پیام‌های متنی
    app.run_polling()

if __name__ == "__main__":
    main()

