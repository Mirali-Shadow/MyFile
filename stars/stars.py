from telethon import Button, events

import config
import database

bot = config.bot

@events.register(events.NewMessage(pattern='⭐️ ثبت سفارش استارز ⭐️'))
async def stars(event):
    
    btn = [
        [Button.text("استارز روی پست"), Button.text("استارز برای اکانت")],
        [Button.text("🔙 بازگشت", resize=True)]
    ]
    
    await bot.send_message(event.chat_id, """🔶 کاربر گرامی به بخش سفارش استارز خوش اومدید 

♦️ توجه : اگر تصمیم بر سفارش استارز برای اکانت خود دارید ، حداقل امتیاز برای سفارش 1000 امتیاز است ❗️""", buttons = btn )


@bot.on(events.NewMessage())
async def choose(event):
    text = event.message
    
    if text == "استارز روی پست" :
        with bot.conversation(event.chat_id) as conv :
            conv.send_message("لطفاً مقدار استارز مورد نیاز خودتون رو بنویسید")
            response1 = conv.get_response()


@bot.on(events.NewMessage(pattern='🔙 بازگشت'))
async def back(event):
    
    start_btn = [
        [Button.text("⭐️ ثبت سفارش استارز ⭐️", resize=True, single_use=True)],
        [Button.text("👤 حساب کاربری"), Button.text("💰 افزایش موجودی")],
        [Button.text("☎️ پشتیبانی")],
        [Button.text("📖")]
    ]
    
    await event.respond("به منوی اصلی بازگشتید ♻️", buttons=start_btn)