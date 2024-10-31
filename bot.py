from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext

# توکن ربات خود را در اینجا قرار دهید
TOKEN = '6414679474:AAHBrTFt5sCbbudkXHu3JvPrR_Pj50T30qs'  # توکن ربات شما

# لینک مستقیم به فایل شما در GitHub
file_url = 'https://raw.githubusercontent.com/Mirali-Shadow/MyFile/2fa16293c554cc38e87fa56831e94d52f0ef3a5d/Seft%20(Djsajjad1%20%26%20BLH%20Remix).mp3'

# تابعی برای ارسال سلام هنگام استارت ربات
def start(update: Update, context: CallbackContext):
    update.message.reply_text('سلام! خوش آمدید به ربات ما!')

# تابعی برای مدیریت پیام‌ها
def handle_message(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id

    # چک کردن آیا پیام شامل لینک اختصاصی است
    if update.message.text == 'https://t.me/shadow_byte_bot?start=getfile':
        # ارسال فایل به کاربر
        context.bot.send_document(chat_id, file_url)
        # هیچ پیامی در اینجا ارسال نمی‌شود

# تابع اصلی برای اجرای ربات
def main():
    # ایجاد آپدیت و دریافت
    updater = Updater(TOKEN, use_context=True)
    
    # ثبت هندلرها
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # شروع ربات
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
