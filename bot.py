import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext, MessageHandler, filters

# توکن بات شما
TOKEN = "6414679474:AAHBrTFt5sCbbudkXHu3JvPrR_Pj50T30qs"

# تابع برای ارسال پیام شیشه‌ای
async def start(update: Update, context: CallbackContext) -> None:
    keyboard = [[InlineKeyboardButton("اشتراک‌گذاری شناسه کاربری", switch_inline_query="")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "برای دریافت فایل، لطفاً شناسه کاربری خود را به اشتراک بگذارید.",
        reply_markup=reply_markup
    )

# تابع برای دریافت شناسه کاربر و ارسال فایل
async def receive_user_id(update: Update, context: CallbackContext) -> None:
    user_id = update.message.text  # دریافت شناسه کاربر از پیام
    chat_id = update.effective_chat.id  # دریافت شناسه چت
    
    await context.bot.send_message(
        chat_id=chat_id,
        text=f"شما شناسه کاربری خود را به اشتراک گذاشتید: {user_id}",
        parse_mode=ParseMode.MARKDOWN
    )
    
    print(f"در حال ارسال فایل به کاربر با شناسه: {chat_id}...")  # چاپ شناسه کاربر
    try:
        file_path = "/workspaces/MyFile/Seft (Djsajjad1 & BLH Remix).mp3"
        # ارسال فایل و ذخیره شناسه پیام
        message = await context.bot.send_document(chat_id=chat_id, document=open(file_path, 'rb'))
        
        await context.bot.send_message(chat_id=chat_id, text="فایل ارسال شد. این فایل بعد از 1 دقیقه پاک خواهد شد.")
        
        await asyncio.sleep(60)  # مکث به مدت 60 ثانیه
        
        await context.bot.delete_message(chat_id=chat_id, message_id=message.message_id)  # حذف پیام حاوی فایل
        print("پیام حاوی فایل پاک شد.")
    except Exception as e:
        print(f"خطا در ارسال فایل: {e}")
        await context.bot.send_message(chat_id=chat_id, text="متاسفانه ارسال فایل ناموفق بود.")

# راه‌اندازی و افزودن هندلرها
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))  # هندلر برای /start
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receive_user_id))  # هندلر برای دریافت شناسه کاربر
    app.run_polling()

if __name__ == "__main__":
    main()
