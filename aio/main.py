from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

bot = Bot(token="7656738137:AAFhyUCOCTvQkje9PoXVQN3UlUv3H2kZlDA")
dp = Dispatcher()

async def get_user_id(username: str):
    try:
        chat = await bot.get_chat(f"@{username}")
        return chat.id
    except Exception as e:
        print(f"Error: {e}")
        return None

@dp.message(Command("id"))
async def handle_id_command(message: types.Message):
    # استخراج یوزرنیم از متن پیام
    args = message.text.split()
    
    if len(args) < 2:
        return await message.reply("❌ لطفا یوزرنیم را وارد کنید!\nمثال: /id @username")
    
    username = args[1].lstrip('@')  # حذف @ از ابتدای یوزرنیم
    
    # دریافت آیدی عددی
    user_id = await get_user_id(username)
    
    if user_id:
        await message.reply(f"🆔 آیدی عددی @{username}:\n<code>{user_id}</code>", parse_mode="HTML")
    else:
        await message.reply("❌ کاربر یافت نشد یا دسترسی محدود است!")

@dp.message(Command("idr"))
async def handle_id_reply(message: types.Message):
    if not message.reply_to_message:
        return await message.reply("❌ لطفا روی یک پیام ریپلای کنید!")
    
    user = message.reply_to_message.from_user
    await message.reply(
        f"👤 اطلاعات کاربر:\n\n"
        f"🆔 آیدی عددی: <code>{user.id}</code>\n"
        f"📛 نام کامل: {user.full_name}\n"
        f"🌐 یوزرنیم: @{user.username}" if user.username else "❌ یوزرنیم ندارد",
        parse_mode="HTML"
    )

if __name__ == "__main__":
    dp.run_polling(bot)
