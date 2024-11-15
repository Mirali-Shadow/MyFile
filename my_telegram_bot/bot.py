import telebot
from database import initialize_database, add_file, get_file

# مقداردهی اولیه دیتابیس
initialize_database()

# ایجاد ربات
bot = telebot.TeleBot("YOUR_BOT_TOKEN_HERE")  # توکن ربات خود را جایگزین کنید

@bot.message_handler(commands=['start'])
def handle_start(message):
    # دریافت پارامتر استارت
    params = message.text.split()
    if len(params) > 1:  # بررسی وجود پارامتر
        file_name = params[1]  # پارامتر دوم به عنوان نام فایل
        file_id = get_file(file_name)

        if file_id:
            bot.send_message(message.chat.id, "در حال ارسال فایل...")
            bot.send_document(message.chat.id, file_id)
        else:
            bot.send_message(message.chat.id, "لینک استارتی شما معتبر نیست.")
    else:
        bot.send_message(message.chat.id, "لطفاً از لینک استارت معتبر استفاده کنید.")

@bot.message_handler(commands=['addfile'])
def handle_addfile(message):
    # دستور افزودن فایل: /addfile file_id file_name
    params = message.text.split()
    if len(params) == 3:
        file_id, file_name = params[1], params[2]
        add_file(file_id, file_name)
        bot.send_message(message.chat.id, f"فایل '{file_name}' با موفقیت اضافه شد.")
    else:
        bot.send_message(message.chat.id, "فرمت دستور نادرست است. مثال: /addfile <file_id> <file_name>")

bot.polling()
