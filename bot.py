import os
import asyncio
from telegram import Update, ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext

# توکن بات شما
TOKEN = "6414679474:AAHBrTFt5sCbbudkXHu3JvPrR_Pj50T30qs"

# تابع برای ارسال پیام شیشه‌ای
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "برای دریافت فایل، لطفاً شناسه کاربری خود را به اشتراک بگذارید.",
        reply_markup={"keyboard": [["اشتراک‌گذاری شناسه کاربری"]],
                      "resize_keyboard": True, "one_time_keyboard": True}
    )

# تابع برای ارسال فایل
async def share_user_id(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_chat.id  # دریافت شناسه کاربر
    await update.message.reply_text(
        "شما شناسه کاربری خود را به اشتراک گذاشتید.",
        parse_mode=ParseMode.MARKDOWN
    )
    
    print(f"در حال ارسال فایل به کاربر با شناسه: {user_id}...")  # چاپ شناسه کاربر
    try:
        file_path = "/workspaces/MyFile/Seft (Djsajjad1 & BLH Remix).mp3"
        with open(file_path, 'rb') as file:
            await context.bot.send_document(chat_id=user_id, document=file)
        
        await context.bot.send_message(chat_id=user_id, text="فایل ارسال شد. این فایل بعد از 1 دقیقه پاک خواهد شد.")
        await asyncio.sleep(60)  # مکث به مدت 60 ثانیه
        
        os.remove(file_path)  # حذف فایل
        print("فایل پاک شد.")
    except Exception as e:
        print(f"خطا در ارسال فایل: {e}")
        await context.bot.send_message(chat_id=user_id, text="متاسفانه ارسال فایل ناموفق بود.")

# راه‌اندازی و افزودن هندلرها
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))  # هندلر برای /start
    app.add_handler(CommandHandler("share_user_id", share_user_id))  # هندلر برای اشتراک‌گذاری شناسه کاربری
    app.run_polling()

if __name__ == "__main__":
    main()
