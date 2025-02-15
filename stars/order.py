from telethon import Button, events

import config
import membership
bot = config.bot

chek = membership.check_membership
sj = membership.send_join_prompt

bot_name = config.bot_name


@events.register(events.NewMessage(pattern=r'💰 افزایش موجودی'))
async def increase(event):
    user_id = event.sender_id
    message_text = event.message.text
    non_member_channels = await chek(user_id)

    btn = [
        [Button.text("🎁 شارژ از طریق رفرال", resize=True), Button.text("🎮 جایزه روزانه")],
        [Button.text("🔙 بازگشت")]
    ]

    if not non_member_channels:
        await event.respond(f"به بخش شارژ حساب کاربری خوش اومدید خوش آمدید!🎉 \nتو این بخش میتونید با انتخاب گزینه مورد نظرتون حساب خودتون رو شارژ کنید", buttons=btn)
    else:
        await sj(user_id, event.chat_id)

@bot.on(events.NewMessage)
async def buy_order(event):
    user_id = event.sender_id
    text = event.message.text

    referral_link = f"https://t.me/{bot_name}?start={user_id}"
    
    file = await bot.upload_file('photo.jpg')

    if text == "🎁 شارژ از طریق رفرال":
        
        await bot.send_file(
            event.chat_id, 
            file, 
            caption=f"""⭐️ جت استارز

💎 دریافت رایگان تعداد نامحدود استارز
🌀 هوشمند ترین بات استارزی  
🔐 پرداخت مطمئن و امن
🔰 پشتیبانی حرفه‌ای و 24 ساعته
{referral_link}
"""
        )
        await event.respond("برای دریافت استارز از طریق رفرال ، پیام بالا رو منتشر کنید .")

    elif text == "🎮 جایزه روزانه":
        await event.respond("کاربر گرامی با عرض پوزش ، این بخش هنوز تکمیل نشده و فعلا فعال نیست\nدر روز های آینده این بخش فعال خواهد شد \nاز صبر و شکیبایی شما متشکریم")

    elif text == "🔙 بازگشت":

        start_btn = [
            [Button.text("⭐️ ثبت سفارش استارز ⭐️", resize=True, single_use=True)],
            [Button.text("👤 حساب کاربری"), Button.text("💰 افزایش موجودی")],
            [Button.text("☎️ پشتیبانی")],
            [Button.text("📖")]
        ]

        await event.respond("به منوی اصلی بازگشتید ♻️", buttons=start_btn)
        