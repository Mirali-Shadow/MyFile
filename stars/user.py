from telethon import Button, events
import database
import config

bot = config.bot

@events.register(events.NewMessage(pattern=r"👤 حساب کاربری"))
async def account(event):
    user_id = event.sender_id
    user_info = database.get_full_user_info(user_id)  # دریافت اطلاعات کامل کاربر
    
    if not user_info:
        await bot.send_message(event.chat_id, "❌ شما هنوز ثبت‌نام نکرده‌اید!")
        return

    points, referrals = user_info[1], user_info[2]
    
    # دریافت نام دعوت‌کننده در صورتی که کاربر از طریق یک نفر دعوت شده باشد
    # inviter_text = f"\n👥 دعوت‌کننده شما: `{inviter_id}`" if inviter_id else ""

    # پیام نهایی برای نمایش اطلاعات حساب کاربری
    account_text = (
        f"📊 **اطلاعات حساب کاربری شما** 📊\n\n"
        f"🏅 **امتیاز:** `{points}`\n"
        f"👥 **تعداد رفرال‌ها:** `{referrals}`"
    )

    buttons = [
        [Button.text("🎯 کسب امتیاز بیشتر"), Button.text("🔙 بازگشت")]
    ]

    await bot.send_message(event.chat_id, account_text)
