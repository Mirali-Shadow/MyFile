import telebot
from pytube import YouTube
import os

# توکن ربات تلگرام خود را جایگزین کنید
bot = telebot.TeleBot("6352712951:AAHtDi_d8NfcmpaYYE9uqX9jZGD-6lsyj40")

# هندلر برای دریافت لینک از کاربر
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(
        message.chat.id, 
        "سلام! لینک یوتیوب را ارسال کنید تا فایل دانلود شود. 🎥"
    )

@bot.message_handler(func=lambda m: True)
def download_youtube_video(message):
    try:
        url = message.text.strip()
        yt = YouTube(url)

        # انتخاب کیفیت بالاترین رزولوشن ویدیو
        stream = yt.streams.get_highest_resolution()
        bot.send_message(message.chat.id, "📥 در حال دانلود ویدیو... لطفا صبر کنید.")
        file_path = stream.download(output_path="downloads")

        # ارسال فایل به کاربر
        with open(file_path, 'rb') as video:
            bot.send_document(message.chat.id, video)

        # حذف فایل پس از ارسال
        os.remove(file_path)
        bot.send_message(message.chat.id, "✅ ویدیو با موفقیت ارسال شد!")

    except Exception as e:
        bot.send_message(message.chat.id, f"❌ خطایی رخ داد:\n{e}")

# شروع ربات
print("ربات در حال اجرا است...")
bot.polling()
