import telebot
import logging
import yt_dlp
import os
import subprocess

API_TOKEN = '7835327718:AAG0aK8WyexgLccGwniQm-SCcp2pFQYhyEI'
bot = telebot.TeleBot(API_TOKEN)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# دستور start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "درود بر شما! لطفا لینک پلی‌لیست یا موزیک را از ساندکلود یا یوتیوب ارسال کنید تا ربات آن را دانلود و ارسال کند.\n ⚠️ در ضمن توجه داشته باشید لینک های یوتیوب فقط به صورت فایل موزیک به شما داده خواهد شد ❗️❕")

# درخواست انتخاب فرمت برای یوتیوب
@bot.message_handler(func=lambda message: "youtube.com" in message.text or "youtu.be" in message.text)
def request_format_choice(message):
    # ذخیره لینک یوتیوب در اطلاعات پیام برای استفاده در مرحله بعد
    bot.user_data = {'youtube_url': message.text}

    # نمایش دکمه‌ها برای انتخاب فرمت
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('MP3', 'MP4')
    bot.reply_to(message, "لطفا فرمت مورد نظر خود را انتخاب کنید (MP3 یا MP4):", reply_markup=markup)
    bot.register_next_step_handler(message, handle_youtube_format_choice)

# ذخیره انتخاب فرمت یوتیوب و دانلود بر اساس فرمت
def handle_youtube_format_choice(message):
    url = bot.user_data.get('youtube_url')
    format_choice = message.text

    if format_choice == "MP3":
        download_and_send_youtube(message, url, 'bestaudio/best')
    elif format_choice == "MP4":
        download_and_send_youtube(message, url, 'bestvideo+bestaudio/best')
    else:
        bot.reply_to(message, "فرمت معتبر نیست. لطفا MP3 یا MP4 را انتخاب کنید.")

# دانلود و ارسال فایل یوتیوب بر اساس فرمت انتخابی
def download_and_send_youtube(message, url, format_choice):
    ydl_opts = {
        'format': format_choice,
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'nocheckcertificate': True,
        'quiet': True,
        'cookiefile' : 'cookie.txt'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            file_name = ydl.prepare_filename(info_dict)
            title = info_dict.get('title', 'Unknown Title')
            artist = info_dict.get('uploader', 'Unknown Artist')

            send_music_file(message, file_name, title, artist)
            os.remove(file_name)

    except Exception as e:
        bot.reply_to(message, f"خطا در دانلود یا ارسال فایل: {str(e)}")

# دانلود از ساندکلود (حالا از پلی‌لیست هم پشتیبانی می‌کند)
def download_from_soundcloud(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'nocheckcertificate': True,
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        if 'entries' in info_dict:  # اگر پلی‌لیست است
            files = []
            for entry in info_dict['entries']:
                file_name = ydl.prepare_filename(entry)
                title = entry.get('title', 'Unknown Title')
                artist = entry.get('uploader', 'Unknown Artist')
                files.append((file_name, title, artist))
            return files
        else:  # اگر یک آهنگ است
            file_name = ydl.prepare_filename(info_dict)
            title = info_dict.get('title', 'Unknown Title')
            artist = info_dict.get('uploader', 'Unknown Artist')
            return [(file_name, title, artist)]

# تابع برای ارسال موزیک به‌صورت موزیک
def send_music_file(message, file_path, title, artist):
    try:
        bot.send_audio(message.chat.id, open(file_path, 'rb'), title=title, performer=artist)
    except Exception as e:
        bot.reply_to(message, f"خطا در ارسال فایل: {str(e)}")

# تابع برای دریافت لینک و ارسال آهنگ‌ها
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    logger.info(f"Received message from {message.from_user.username}")
    
    if "soundcloud.com" in message.text:
        url = message.text
        bot.reply_to(message, 'در حال دانلود موزیک‌ها از ساندکلود...')
        try:
            files = download_from_soundcloud(url)
            if files:
                for file_path, title, artist in files:
                    send_music_file(message, file_path, title, artist)
                    os.remove(file_path)
            else:
                bot.reply_to(message, "خطا در دانلود یا ارسال فایل.")
        except Exception as e:
            bot.reply_to(message, f"خطا در دانلود یا ارسال فایل: {str(e)}")
    
    elif "youtube.com" in message.text or "youtu.be" in message.text:
        request_format_choice(message)

# اجرای ربات
bot.polling()
