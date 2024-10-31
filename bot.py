from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext

# توکن بات شما
TOKEN = "6414679474:AAHBrTFt5sCbbudkXHu3JvPrR_Pj50T30qs"

# تابع برای ارسال فایل به کاربر
async def start(update: Update, context: CallbackContext) -> None:
    # چک کردن پارامترهای ورودی
    if context.args and context.args[0] == "getfile2":
        await get_file_2(update, context)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="سلام! برای دریافت فایل، لینک مخصوص را ارسال کنید.")

# تابع برای ارسال فایل دوم
async def get_file_2(update: Update, context: CallbackContext) -> None:
    print("در حال ارسال فایل از لینک getfile2...")
    try:
        await context.bot.send_document(chat_id=update.effective_chat.id,
                                         document=open("/workspaces/MyFile/AnotherFile.mp3", 'rb'))  # مسیر فایل
        print("فایل دوم ارسال شد.")
    except Exception as e:
        print(f"خطا در ارسال فایل: {e}")
        await context.bot.send_message(chat_id=update.effective_chat.id, text="متاسفانه ارسال فایل دوم ناموفق بود.")

# راه‌اندازی و افزودن هندلرها
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))  # هندلر برای /start
    app.run_polling()

if __name__ == "__main__":
    main()
