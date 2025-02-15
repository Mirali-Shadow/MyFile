import yt_dlp 
import os

def handle_soundcloud_link(bot, message):
    url = message.text
    bot.reply_to(message, 'در حال دانلود موزیک‌ها از ساندکلود...')
    try:
        files = download_from_soundcloud(url)
        if files:
            for file_path, title, artist in files:
                send_music_file(bot, message, file_path, title, artist)
                os.remove(file_path)
        else:
            bot.reply_to(message, "خطا در دانلود یا ارسال فایل.")
    except Exception as e:
        bot.reply_to(message, f"خطا در دانلود یا ارسال فایل: {str(e)}")

def download_from_soundcloud(url):
    ydl_opts = {'format': 'bestaudio/best', 'outtmpl': 'downloads/%(title)s.%(ext)s', 'quiet': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        if 'entries' in info_dict:
            return [(ydl.prepare_filename(entry), entry.get('title', 'Unknown Title'), entry.get('uploader', 'Unknown')) for entry in info_dict['entries']]
        else:
            return [(ydl.prepare_filename(info_dict), info_dict.get('title', 'Unknown Title'), info_dict.get('uploader', 'Unknown'))]

def send_music_file(bot, message, file_path, title, artist):
    bot.send_audio(message.chat.id, open(file_path, 'rb'), title=title, performer=artist)
