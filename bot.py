from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext

# توکن بات شما
TOKEN = "6414679474:AAHBrTFt5sCbbudkXHu3JvPrR_Pj50T30qs"

# تابع برای ارسال فایل به کاربر
async def start(update: Update, context: CallbackContext) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id, text="سلام! برای دریافت فایل، لینک مخصوص را ارسال کنید.")

# تابع برای مدیریت پیام‌ها
async def handle_message(update: Update, context: CallbackContext) -> None:
    # لینک اختصاصی که کاربر باید ارسال کند
    special_link = "https://t.me/shadow_byte_bot?start=getfil"

    # چاپ متن پیام دریافتی
    print(f"متن دریافتی: {update.message.text}")

    if update.message.text == special_link:
        print("در حال ارسال فایل...")
        try:
            await context.bot.send_document(chat_id=update.effective_chat.id,
                                             document=open("/workspaces/MyFile/Pishro - Tamum Shode (featuring Kamyar).mp3", 'rb'))
            print("فایل ارسال شد.")
        except Exception as e:
            print(f"خطا در ارسال فایل: {e}")
            await context.bot.send_message(chat_id=update.effective_chat.id, text="متاسفانه ارسال فایل ناموفق بود.")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="لطفاً لینک صحیح را ارسال کنید.")

# راه‌اندازی و افزودن هندلرها
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))  # مدیریت پیام‌های متنی
    app.run_polling()

if __name__ == "__main__":
    main()
