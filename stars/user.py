from telethon import Button, events
import database
import config

bot = config.bot

@events.register(events.NewMessage(pattern=r"👤 حساب کاربری"))
async def account(event):
    user_id = event.sender_id
    user_info = database.get_full_user_info(user_id)
    
    if not user_info:
        await bot.send_message(event.chat_id, "❌ شما هنوز ثبت‌نام نکرده‌اید!")
        return

    points, referrals = user_info[1], user_info[2]

    account_text = (
        f"📊 **اطلاعات حساب کاربری شما** 📊\n\n"
        f"🏅 **امتیاز:** `{points}`\n"
        f"👥 **تعداد رفرال‌ها:** `{referrals}`"
    )

    await bot.send_message(event.chat_id, account_text)
