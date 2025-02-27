from telethon import TelegramClient

api_id = 21266027 
api_hash = "8563c2456fa80793ccf835eec5be4a72" 
token = "7656738137:AAFhyUCOCTvQkje9PoXVQN3UlUv3H2kZlDA"
owner_id = 7313704680
support_id = 7013701883

bot_name = "shadofficialbot"

bot = TelegramClient("STARS", api_id, api_hash)
bot.start(bot_token=token)