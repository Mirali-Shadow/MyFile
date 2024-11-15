import telebot
from telebot import types
from datetime import datetime

bot = telebot.TeleBot("6352712951:AAHtDi_d8NfcmpaYYE9uqX9jZGD-6lsyj40")

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.from_user.id
    username = message.from_user.username or "No Username"  # اگر یوزرنیم نداشت، مقدار پیش‌فرض
    first_name = message.from_user.first_name or "No First Name"
    last_name = message.from_user.last_name or "No Last Name"

    # تاریخ و زمان فعلی
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # دریافت پارامتر start از پیام
    if message.text == '/start 1568d32k74':
        # اگر لینک درست باشد، فایل ارسال می‌شود
        file_url = "https://drive.google.com/uc?export=download&id=12aZaNkF-fWTg_5TadLY7KRJL8b6gar3x"
        bot.send_message(message.chat.id, "در حال ارسال فایل...")
        bot.send_document(message.chat.id, file_url)
    elif message.text == '/start getfil':
        file_url1 = "https://drive.google.com/uc?export=download&id=1WnXT_aBpxRDtMZ5GELT2YnCiEWSAqNtD"
        bot.send_message(message.chat.id, "در حال ارسال فایل شما...")
        bot.send_document(message.chat.id, file_url1)
    else:
        # اگر لینک اشتباه باشد
        bot.send_message(message.chat.id, "لینک استارتی شما معتبر نیست. لطفاً لینک درست را امتحان کنید.")
        

    # چاپ اطلاعات در ترمینال (قبل از دریافت شماره)
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

bot.polling()
