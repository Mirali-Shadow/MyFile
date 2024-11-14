
import telebot
import logging
from youtube_module import handle_youtube_link
from soundcloud_module import handle_soundcloud_link

API_TOKEN = '7835327718:AAG0aK8WyexgLccGwniQm-SCcp2pFQYhyEI'
bot = telebot.TeleBot(API_TOKEN)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# دستور start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "درود بر شما! لطفا لینک پلی‌لیست یا موزیک را از ساندکلود یا یوتیوب ارسال کنید تا ربات آن را دانلود و ارسال کند.")

# هندلر اصلی برای شناسایی لینک و توزیع به فایل‌های دیگر
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    logger.info(f"Received message from {message.from_user.username}")
    
    if "soundcloud.com" in message.text:
        handle_soundcloud_link(bot, message)
    
    elif "youtube.com" in message.text or "youtu.be" in message.text:
        handle_youtube_link(bot, message)

# اجرای ربات
bot.polling()
