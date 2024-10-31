import os
import asyncio
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext, MessageHandler, filters

# توکن بات شما
TOKEN = "6414679474:AAHBrTFt5sCbbudkXHu3JvPrR_Pj50T30qs"

# تابع برای ارسال پیام خوش آمدگویی
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "برای دریافت فایل، لطفاً شناسه کاربری خود را به صورت @example_name ارسال کنید."
    )

# تابع برای ارسال دوباره فایل
async def send_file(chat_id: int, context: CallbackContext):
    file_path = "/workspaces/MyFile/Seft (Djsajjad1 & BLH Remix).mp3"
    message = await context.bot.send_document(chat_id=chat_id, document=open(file_path, 'rb'))
    
    await context.bot.send_message(chat_id=chat_id, text="فایل ارسال شد. این فایل بعد از 1 دقیقه پاک خواهد شد.")

    await asyncio.sleep(60)  # مکث به مدت 60 ثانیه

    await context.bot.delete_message(chat_id=chat_id, message_id=message.message_id)  # حذف پیام حاوی فایل
    await context.bot.send_message(chat_id=chat_id, text="فایل پاک شد. برای دریافت مجدد رسانه [کلیک کنید](https://t.me/shadow_byte_bot?start=getfile2)", parse_mode=ParseMode.MARKDOWN)

# تابع برای دریافت شناسه کاربر و ارسال فایل
async def receive_user_id(update: Update, context: CallbackContext) -> None:
    user_id = update.message.text.strip()  # دریافت شناسه کاربر از پیام
    chat_id = update.effective_chat.id  # دریافت شناسه چت
    
    # بررسی اینکه آیا شناسه کاربر به درستی فرستاده شده است
    if user_id.startswith("@"):
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"شما شناسه کاربری خود را به اشتراک گذاشتید: {user_id}",
            parse_mode=ParseMode.MARKDOWN
        )
        
        print(f"در حال ارسال فایل به کاربر با شناسه: {chat_id}...")  # چاپ شناسه کاربر
        await send_file(chat_id, context)  # ارسال فایل
    else:
        await context.bot.send_message(
            chat_id=chat_id,
            text="لطفاً شناسه کاربری خود را به صورت @example_name ارسال کنید."
        )

# راه‌اندازی و افزودن هندلرها
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))  # هندلر برای /start
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receive_user_id))  # هندلر برای دریافت شناسه کاربر
    app.run_polling()

if __name__ == "__main__":
    main()
