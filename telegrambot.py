from database import create_table, get_file_link_from_db
import telebot
from datetime import datetime

API_TOKEN = '6352712951:AAHtDi_d8NfcmpaYYE9uqX9jZGD-6lsyj40'
bot = telebot.TeleBot(API_TOKEN)

# ایجاد جدول اگر وجود نداشته باشد
create_table()

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.from_user.id
    username = message.from_user.username or "No Username"
    first_name = message.from_user.first_name or "No First Name"
    last_name = message.from_user.last_name or "No Last Name"
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if message.text == '/start':
        bot.send_message(
            message.chat.id,
            f"سلام {first_name}!\nبه ربات خوش آمدید. 🌟\nلطفاً دستور درست را وارد کنید."
        )
        print(f"[{current_time}] User started the bot (without any command): {first_name} {last_name}")
    else:
        file_link = get_file_link_from_db(message.text)
        if file_link:
            bot.send_message(message.chat.id, "در حال ارسال فایل...")
            bot.send_document(message.chat.id, file_link)
            print(f"[{current_time}] User {username} ({first_name} {last_name}) requested and downloaded: {message.text}")
        else:
            bot.send_message(message.chat.id, "لینک استارتی شما معتبر نیست. لطفاً لینک درست را امتحان کنید.")

    print(f"[{current_time}] User started the bot:")
    print(f"  ID: {user_id}")
    print(f"  Username: @{username}")
    print(f"  Name: {first_name} {last_name}")

# راه‌اندازی ربات
bot.polling()
