from database import create_table, get_file_link_from_db
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime

API_TOKEN = '6414679474:AAHBrTFt5sCbbudkXHu3JvPrR_Pj50T30qs'
bot = telebot.TeleBot(API_TOKEN)

# ایجاد جدول اگر وجود نداشته باشد
create_table()

# لیست کانال‌ها با لینک دعوت خصوصی
CHANNELS = [
    {'invite_link': 'https://t.me/MiRALi_ViBE', 'username': '@MiRALi_ViBE', 'name': 'کانال اول'},
    {'invite_link': 'https://t.me/SHADOW_R3', 'username': '@SHADOW_R3', 'name': 'کانال دوم'},
    {'invite_link': 'https://t.me/+GrBtMvoIEJxjMGFk', 'username': '@mirali_vibe', 'name': 'کانال سوم'}
]

# پیام خوشامدگویی
WELCOME_MESSAGE = """
سلام! 👋
برای استفاده از این ربات، لطفاً ابتدا در کانال‌های زیر عضو شوید:
"""

# بررسی عضویت کاربر در کانال عمومی
def is_user_in_channel(user_id, channel_username):
    try:
        status = bot.get_chat_member(channel_username, user_id).status
        return status in ['member', 'administrator', 'creator']
    except Exception:
        return False

# بررسی عضویت کاربر در تمام کانال‌ها
def check_all_channels(user_id):
    not_joined = []
    for channel in CHANNELS:
        if not is_user_in_channel(user_id, channel['username']):
            not_joined.append(channel)
    return not_joined

# ارسال لینک دعوت و دکمه تأیید عضویت
def send_channels_to_user(chat_id):
    markup = InlineKeyboardMarkup()
    for channel in CHANNELS:
        markup.add(InlineKeyboardButton(text=f"عضویت در {channel['name']}", url=channel['invite_link']))
    markup.add(InlineKeyboardButton(text="تأیید عضویت", callback_data="check_membership"))
    bot.send_message(chat_id, WELCOME_MESSAGE, reply_markup=markup)

# هندلر دستور /start
# هندلر عمومی برای همه پیام‌ها
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    user_id = message.from_user.id
    username = message.from_user.username or "No Username"
    first_name = message.from_user.first_name or "No First Name"
    last_name = message.from_user.last_name or "No Last Name"
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # بررسی عضویت کاربر در کانال‌ها
    not_joined = check_all_channels(user_id)

    if not_joined:
        # اگر عضو همه کانال‌ها نشده باشد، پیامی به کاربر ارسال می‌شود که می‌گوید ابتدا باید در کانال‌ها عضو شود
        message_text = "❌ شما هنوز در کانال‌های زیر عضو نشده‌اید:\n"
        for channel in not_joined:
            message_text += f"{channel['name']} - {channel['invite_link']}\n"

        # ایجاد دوباره دکمه‌ها برای استعلام عضویت
        markup = InlineKeyboardMarkup()
        for channel in not_joined:
            markup.add(InlineKeyboardButton(text=f"عضویت در {channel['name']}", url=channel['invite_link']))
        markup.add(InlineKeyboardButton(text="تأیید عضویت", callback_data="check_membership"))

        # ارسال پیامی به کاربر که باید ابتدا در کانال‌ها عضو شود
        bot.send_message(message.chat.id, message_text, reply_markup=markup)
        return  # از اینجا به بعد هیچ کاری انجام نمی‌دهیم چون کاربر باید در کانال‌ها عضو شود.

    # اگر کاربر عضو تمام کانال‌ها باشد، کد زیر اجرا می‌شود.
    if message.text == '/start':
        send_channels_to_user(message.chat.id)
        print(f"[{current_time}] User started the bot: {first_name} {last_name}")

    else:
        file_link = get_file_link_from_db(message.text)
        if file_link:
            bot.send_message(message.chat.id, "در حال ارسال فایل...")
            bot.send_document(message.chat.id, file_link)
            print(f"[{current_time}] User {username} ({first_name} {last_name}) requested and downloaded: {message.text}")
        else:
            bot.send_message(message.chat.id, "لینک استارتی شما معتبر نیست. لطفاً لینک درست را امتحان کنید.")

    print(f"[{current_time}] User sent a message:")
    print(f"  ID: {user_id}")
    print(f"  Username: @{username}")
    print(f"  Name: {first_name} {last_name}")

# هندلر دکمه "تأیید عضویت"
@bot.callback_query_handler(func=lambda call: call.data == "check_membership")
def handle_membership_check(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    # بررسی عضویت کاربر در همه کانال‌ها
    not_joined = check_all_channels(user_id)
    
    if not_joined:
        message = "❌ شما هنوز در کانال‌های زیر عضو نشده‌اید:\n"
        for channel in not_joined:
            message += f""
        
        # ایجاد دوباره دکمه‌ها برای استعلام عضویت
        markup = InlineKeyboardMarkup()
        for channel in not_joined:
            markup.add(InlineKeyboardButton(text=f"عضویت در {channel['name']}", url=channel['invite_link']))
        markup.add(InlineKeyboardButton(text="تأیید عضویت", callback_data="check_membership"))

        # ویرایش پیام شیشه‌ای و بازگرداندن دکمه‌ها
        bot.edit_message_text(
            text=message,
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=markup
        )
    else:
        message = "✅ شما عضو همه کانال‌ها هستید و می‌توانید از ربات استفاده کنید!"
        
        # ویرایش پیام شیشه‌ای برای اعلام تأیید عضویت
        bot.edit_message_text(
            text=message,
            chat_id=chat_id,
            message_id=message_id
        )
# راه‌اندازی ربات
bot.polling()
