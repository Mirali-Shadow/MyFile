import telebot
import json
from datetime import datetime
from telebot import types

API_TOKEN = '6352712951:AAHtDi_d8NfcmpaYYE9uqX9jZGD-6lsyj40'
bot = telebot.TeleBot(API_TOKEN)

# بارگذاری داده‌های فایل‌ها از فایل JSON
def load_files_from_json():
    with open('files.json', 'r', encoding='utf-8') as file:
        return json.load(file)

files_data = load_files_from_json()

# دریافت لینک فایل از JSON بر اساس دستور
def get_file_link_from_json(command):
    for file in files_data:
        if file['command'] == command:
            return file['file_id'], file['file_name']
    return None, None

# دستور برای ارسال فایل از لینک دانلود مستقیم
@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.from_user.id
    username = message.from_user.username or "No Username"
    first_name = message.from_user.first_name or "No First Name"
    last_name = message.from_user.last_name or "No Last Name"

    # تاریخ و زمان فعلی
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # دریافت لینک و نام فایل بر اساس دستور
    file_id, file_name = get_file_link_from_json(message.text)

    if file_id:
        file_url = f"https://drive.google.com/uc?export=download&id={file_id}"
        bot.send_message(message.chat.id, f"در حال ارسال {file_name}...")
        bot.send_document(message.chat.id, file_url)  # ارسال فایل از لینک
        print(f"[{current_time}] User {username} ({first_name} {last_name}) requested and downloaded: {file_name} (ID: {file_id})")
    else:
        # اگر لینک اشتباه باشد
        bot.send_message(message.chat.id, "لینک استارتی شما معتبر نیست.")
        print(f"[{current_time}] Invalid command: {message.text}")

    # ارسال اطلاعات کاربر
    print(f"[{current_time}] User started the bot:")
    print(f"  ID: {user_id}")
    print(f"  Username: @{username}")
    print(f"  Name: {first_name} {last_name}")

    # ارسال پیام به کاربر برای درخواست شماره
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    contact_button = types.KeyboardButton(text="ارسال شماره", request_contact=True)
    markup.add(contact_button)
    bot.send_message(
        message.chat.id,
        f"سلام {first_name}!\nبه ربات خوش آمدید. 🌟\n\nیوزرنیم شما: @{username if username != 'No Username' else 'نامشخص'}\nلطفا شماره خود را ارسال کنید.",
        reply_markup=markup
    )

@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    user_id = message.from_user.id
    username = message.from_user.username or "No Username"
    first_name = message.from_user.first_name or "No First Name"
    last_name = message.from_user.last_name or "No Last Name"

    # شماره تماس
    contact_number = message.contact.phone_number

    # تاریخ و زمان فعلی
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # چاپ اطلاعات در ترمینال (بعد از دریافت شماره)
    print(f"[{current_time}] User provided their contact:")
    print(f"  ID: {user_id}")
    print(f"  Username: @{username}")
    print(f"  Name: {first_name} {last_name}")
    print(f"  Contact Number: {contact_number}")

    # ارسال تایید به کاربر
    bot.send_message(
        message.chat.id,
        f"شماره شما: {contact_number}\nتایید شد! ✅"
    )

# راه‌اندازی ربات
bot.polling()
