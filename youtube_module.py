import yt_dlp
import os
import telebot

# درخواست فرمت و کیفیت فایل یوتیوب
def handle_youtube_link(bot, message):
    url = message.text  # ذخیره لینک در یک متغیر محلی

    # ساخت اینلاین کیبورد برای انتخاب فرمت
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(
        telebot.types.InlineKeyboardButton('MP3', callback_data=f'format_MP3_{url}'),
        telebot.types.InlineKeyboardButton('MP4', callback_data=f'format_MP4_{url}')
    )
    bot.reply_to(message, "لطفا فرمت مورد نظر خود را انتخاب کنید:", reply_markup=markup)

# هندلر برای انتخاب فرمت
def handle_format_choice_callback(bot, call):
    url = call.data.split('_')[-1]
    format_choice = call.data.split('_')[1]

    if format_choice == "MP3":
        download_and_send_youtube_audio(bot, call.message, url, 'bestaudio/best')
    elif format_choice == "MP4":
        # ساخت اینلاین کیبورد برای انتخاب کیفیت
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(
            telebot.types.InlineKeyboardButton('720p', callback_data=f'quality_720p_{url}'),
            telebot.types.InlineKeyboardButton('480p', callback_data=f'quality_480p_{url}'),
            telebot.types.InlineKeyboardButton('360p', callback_data=f'quality_360p_{url}')
        )
        bot.edit_message_text("لطفا کیفیت ویدیو را انتخاب کنید:", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)

# هندلر برای انتخاب کیفیت
def handle_quality_choice_callback(bot, call):
    url = call.data.split('_')[-1]
    quality = call.data.split('_')[1]

    format_choice = {
        "720p": 'bestvideo[height<=720]+bestaudio/best',
        "480p": 'bestvideo[height<=480]+bestaudio/best',
        "360p": 'bestvideo[height<=360]+bestaudio/best'
    }.get(quality)

    if format_choice:
        download_and_send_youtube_video(bot, call.message, url, format_choice)

# دانلود و ارسال فایل صوتی یوتیوب
def download_and_send_youtube_audio(bot, message, url, format_choice):
    ydl_opts = {
        'format': f'{format_choice}/mp4',  # اضافه کردن /mp4 برای انتخاب فرمت MP4 به‌جای WebM
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'nocheckcertificate': True,
        'quiet': True,
        'cookiefile': 'cookie.txt'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        file_name = ydl.prepare_filename(info_dict)
        bot.send_audio(message.chat.id, open(file_name, 'rb'), title=info_dict.get('title', 'Unknown'))
        os.remove(file_name)

# دانلود و ارسال فایل ویدیویی یوتیوب
def download_and_send_youtube_video(bot, message, url, format_choice):
    
    ydl_opts = {
        'format': format_choice,
        # 'default_search': 'ytsearch',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'nocheckcertificate': True,
        'quiet': True,
        'cookiefile': 'cookie.txt'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        file_name = ydl.prepare_filename(info_dict)
        bot.send_video(message.chat.id, open(file_name, 'rb'), caption=info_dict.get('title', 'Unknown'))
        os.remove(file_name)

# اتصال هندلرهای callback به دکمه‌های اینلاین
bot = telebot.TeleBot('7835327718:AAG0aK8WyexgLccGwniQm-SCcp2pFQYhyEI')

@bot.message_handler(func=lambda message: 'youtube.com' in message.text or 'youtu.be' in message.text)
def youtube_link_handler(message):
    handle_youtube_link(bot, message)

@bot.callback_query_handler(func=lambda call: call.data.startswith('format_'))
def callback_format_choice(call):
    handle_format_choice_callback(bot, call)

@bot.callback_query_handler(func=lambda call: call.data.startswith('quality_'))
def callback_quality_choice(call):
    handle_quality_choice_callback(bot, call)

bot.polling()
