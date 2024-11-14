import telebot
import logging
import yt_dlp
import os
import subprocess

# توکن ربات خود را وارد کنید
API_TOKEN = '7835327718:AAG0aK8WyexgLccGwniQm-SCcp2pFQYhyEI'
bot = telebot.TeleBot(API_TOKEN)

# تنظیمات لاگینگ برای دیباگ
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# دستور start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "درود بر شما! لطفا لینک پلی‌لیست یا موزیک را از ساندکلود یا یوتیوب ارسال کنید تا ربات آن را دانلود و ارسال کند.\n ⚠️ در ضمن توجه داشته باشید لینک های یوتیوب فقط به صورت فایل موزیک به شما داده خواهد شد ❗️❕")

# تابع دانلود از ساندکلود (برای یک آهنگ)
def download_from_soundcloud(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'nocheckcertificate': True,
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        file_name = ydl.prepare_filename(info_dict)
        title = info_dict.get('title', 'Unknown Title')
        artist = info_dict.get('uploader', 'Unknown Artist')
        return file_name, title, artist

# تابع دانلود از یوتیوب (برای یک آهنگ)
def download_from_youtube(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'nocheckcertificate': True,
        'quiet': True,
        'cookiefile': 'cookie.txt',  # مسیر فایل کوکی‌ها برای عبور از CAPTCHA
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        file_name = ydl.prepare_filename(info_dict)
        title = info_dict.get('title', 'Unknown Title')
        artist = info_dict.get('uploader', 'Unknown Artist')
        return file_name, title, artist

# تابع دانلود از اسپاتیفای (برای یک آهنگ)
def download_from_spotify(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'nocheckcertificate': True,
        'quiet': True,
        'extractaudio': True,  # تبدیل به فایل صوتی
        'audioquality': 1,  # بهترین کیفیت
        'geo_bypass': True,  # عبور از محدودیت‌های جغرافیایی
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        file_name = ydl.prepare_filename(info_dict)
        title = info_dict.get('title', 'Unknown Title')
        artist = info_dict.get('uploader', 'Unknown Artist')
        return file_name, title, artist

# تابع برای تبدیل فایل به MP3 (در صورت نیاز)
def convert_to_mp3(file_path):
    output_path = file_path.rsplit('.', 1)[0] + '.mp3'
    try:
        subprocess.run(['ffmpeg', '-i', file_path, output_path], check=True)
        os.remove(file_path)  # حذف فایل اصلی پس از تبدیل
        return output_path
    except Exception as e:
        logger.error(f"خطا در تبدیل فایل: {e}")
        return None

# تابع برای ارسال موزیک به‌صورت موزیک (نه ویس)
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
            file_path, title, artist = download_from_soundcloud(url)
            if file_path:
                send_music_file(message, file_path, title, artist)
                os.remove(file_path)
            else:
                bot.reply_to(message, "خطا در دانلود یا ارسال فایل.")
        except Exception as e:
            bot.reply_to(message, f"خطا در دانلود یا ارسال فایل: {str(e)}")
    
    elif "youtube.com" in message.text or "youtu.be" in message.text:
        url = message.text
        bot.reply_to(message, 'در حال دانلود موزیک‌ها از یوتیوب...')
        try:
            file_path, title, artist = download_from_youtube(url)
            if file_path:
                send_music_file(message, file_path, title, artist)
                os.remove(file_path)
            else:
                bot.reply_to(message, "خطا در دانلود یا ارسال فایل.")
        except Exception as e:
            bot.reply_to(message, f"خطا در دانلود یا ارسال فایل: {str(e)}")
    
# اجرای ربات
bot.polling()
