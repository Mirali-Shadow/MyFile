from telethon import Button, TelegramClient
from telethon.tl import functions, types

admin_id = 1778976582
# admin_id = 7313704680

api_id = 21266027                 # api id 
api_hash = "8563c2456fa80793ccf835eec5be4a72"                  # api hash
token = "7656738137:AAFhyUCOCTvQkje9PoXVQN3UlUv3H2kZlDA"                     # bot token (from bot father)
channel_id = -1002296724085                   # آیدی عددی کانالی که قراره پست ها توش قرار بگیرن

bot = TelegramClient("Gift", api_id, api_hash)
bot.start(bot_token=token)

CHANNEL_ID = "-1002296724085"               # آیدی کانال قفل شده
CHANNEL_LINK = "https://t.me/iCaspyan"       # لینک کانال قفل شده
CHANNEL_NAME = "Test"                # نام برای دکمه شیشه‌ای کانال قفل شده
