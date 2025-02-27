from telethon import TelegramClient, events, types

# اطلاعات ربات (جایگزین کنید)
API_ID = 21266027
API_HASH = "8563c2456fa80793ccf835eec5be4a72"
BOT_TOKEN = "7656738137:AAFhyUCOCTvQkje9PoXVQN3UlUv3H2kZlDA"

bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

@bot.on(events.NewMessage(incoming=True))
async def handle_file(event):
    if event.photo:
        file = event.photo
        file_id = file.id
        access_hash = file.access_hash
        file_reference = file.file_reference  # ذخیره کردن file_reference جدید

        message = f"""
📂 اطلاعات فایل شما:
📌 **ID:** `{file_id}`
📌 **Access Hash:** `{access_hash}`
📌 **File Reference:** `{base64.b64encode(file_reference).decode()}`
"""

        await event.respond(message)

@bot.on(events.NewMessage(pattern="/send_file"))
async def send_file(event):
    try:
        photo_id = 5023943780549635511
        access_hash = 7767204989237424063
        file_reference_base64 = "AQAAJIxntymidzdTYtT1+grLIhezOo+tug=="

        file_reference = base64.b64decode(file_reference_base64)

        file_input = types.InputPhoto(id=photo_id, access_hash=access_hash, file_reference=file_reference)

        await bot.send_file(
            event.chat_id, 
            file_input, 
            caption="📂 این همان فایل ذخیره‌شده شماست!"
        )
    
    except Exception as e:
        await event.respond(f"❌ خطا در ارسال فایل: {str(e)}")

import base64

@bot.on(events.NewMessage(pattern="/get_photo_id"))
async def get_photo_id(event):
    if event.message.photo:
        photo = event.message.photo
        file_reference_b64 = base64.b64encode(photo.file_reference).decode() 
        await event.reply(f"📸 **Photo ID:** `{photo.id}`\n"
                          f"🔑 **Access Hash:** `{photo.access_hash}`\n"
                          f"📄 **File Reference:** `{file_reference_b64}`")
    else:
        await event.reply("❌ لطفاً یک عکس ارسال کنید.")

@bot.on(events.NewMessage(pattern=r"/send"))
async def sendto(event):

    photo_id = 5023943780549635511
    access_hash = 7767204989237424063
    file_reference=b'\x01\x00\x00$tg\xb7!\xe9\x8f\x03J\x0b\xd9\x8d\xd9"\xa6\x8c%\xf6\xaa\\Y\xfc'
    input_photo = types.InputPhoto(id=photo_id, access_hash=access_hash, file_reference=file_reference)

    await bot.send_file(event.chat_id, input_photo, caption="📸 این عکس شماست!")

@bot.on(events.NewMessage(pattern="/send_photo"))
async def send_photo(event):
    try:
        args = event.message.text.split()
        if len(args) < 4:
            await event.reply("❌ فرمت نادرست! مثال: `/send_photo photo_id access_hash file_reference`")
            return
        
        photo_id = int(args[1])
        access_hash = int(args[2])
        file_reference = base64.b64decode(args[3]) 

        file_input = types.InputPhoto(id=photo_id, access_hash=access_hash, file_reference=file_reference)

        await bot.send_file(
            event.chat_id, 
            file_input, 
            caption="⭐️ این عکس از `file_id` ارسال شد!"
        )

    except Exception as e:
        await event.reply(f"❌ خطا: {str(e)}")

print("✅ ربات فعال شد!")
bot.run_until_disconnected()


