from telethon import Button, events
import config
import database

bot = config.bot
OWNER_ID = config.owner_id 
CHANNEL_ID = -1002498118094 
STARS = 20 


start_btn = [
        [Button.text("⭐️ ثبت سفارش استارز ⭐️", resize=True, single_use=True)],
        [Button.text("👤 حساب کاربری"), Button.text("💰 افزایش موجودی")],
        [Button.text("☎️ پشتیبانی")],
        [Button.text("📖")]
    ]


@events.register(events.NewMessage(pattern='⭐️ ثبت سفارش استارز ⭐️'))
async def stars(event):
    btn = [
        [Button.text("استارز روی پست"), Button.text("استارز برای اکانت")],
        [Button.text("🔙 بازگشت", resize=True)]
    ]
    await bot.send_message(event.chat_id, """🔶 کاربر گرامی به بخش سفارش استارز خوش اومدید 

♦️ توجه: حداقل امتیاز برای سفارش استارز برای اکانت 1000 امتیاز است ❗️""", buttons=btn)

@bot.on(events.NewMessage())
async def choose(event):
    text = event.message.text
    user_id = event.sender_id
    user_points = database.get_user_points(user_id)
    
    if text == "استارز روی پست":
        async with bot.conversation(event.chat_id) as conv:
            await conv.send_message("لطفاً مقدار استارز مورد نیاز خودتون رو بنویسید")
            response1 = await conv.get_response()
            
            try:
                quantity = int(response1.text)
                if quantity <= 0:
                    await conv.send_message("❌ مقدار وارد شده نامعتبر است!")
                    return
            except ValueError:
                await conv.send_message("❌ لطفاً یک عدد معتبر وارد کنید!")
                return
            
            await conv.send_message("لطفاً لینک پست مورد نظر را ارسال کنید")
            response2 = await conv.get_response()
            post_link = response2.text
            
            total_price = quantity * STARS
            
            if user_points < total_price:
                await conv.send_message("❌ امتیاز شما کافی نیست!")
                return
            
            database.decrease_user_points_for_order(user_id, total_price)
            database.add_order(user_id, "استارز روی پست", quantity, total_price, post_link)
            
            buttons = [
                [Button.url("مشاهده پست", post_link)],
                [Button.inline("✅ انجام شد", data=f"done_{user_id}_{quantity}_{total_price}")]
            ]
            
            await bot.send_message(OWNER_ID, f"📢 سفارش جدید استارز:\n👤 ID: {user_id}\n📊 Quantity: {quantity}\n💰 Total Price: {total_price} امتیاز", buttons=buttons)
            await conv.send_message("✅ سفارش شما ثبت شد و در حال پردازش است.")

    elif text == "استارز برای اکانت":
        if user_points < 1000:
            await bot.send_message(event.chat_id, "❌ امتیاز شما کافی نیست! حداقل 1000 امتیاز نیاز دارید.")
            return
        
        user_can = user_points / 20
        
        async with bot.conversation(event.chat_id) as conv:
            await conv.send_message(f"شما {user_points} امتیاز دارید. مقدار مورد نظر خود را (بین 50 تا {user_can}) وارد کنید:")
            response1 = await conv.get_response()
            
            try:
                quantity = int(response1.text)
                if quantity < 50 or quantity > user_points:
                    await conv.send_message("❌ مقدار وارد شده نامعتبر است!")
                    return
            except ValueError:
                await conv.send_message("❌ لطفاً یک عدد معتبر وارد کنید!")
                return
            
            await conv.send_message("لطفاً یوزرنیم اکانت خود را با @ وارد کنید:")
            response2 = await conv.get_response()
            username = response2.text
            
            database.decrease_user_points_for_order(user_id, quantity)
            database.add_order(user_id, "استارز برای اکانت", quantity, quantity, username)
            
            buttons = [
                [Button.inline("✅ انجام شد", data=f"done_account_{user_id}_{quantity}")]
            ]
            
            await bot.send_message(OWNER_ID, f"📢 سفارش جدید استارز برای اکانت:\n👤 ID: {user_id}\n📊 Quantity: {quantity}\n🔗 Username: {username}", buttons=buttons)
            await conv.send_message("✅ سفارش شما ثبت شد و در حال پردازش است.")

@bot.on(events.CallbackQuery(pattern=b"done_\d+_\d+_\d+"))
async def order_done(event):
    data = event.data.decode().split('_')
    user_id, quantity, total_price = data[1], data[2], data[3]
    
    masked_user_id = str(user_id)[:4] + "****"  # ماسک کردن آی‌دی
    
    message = f"""🛍 سفارش موفق استارز بر روی پست:
👤 ID: {masked_user_id}
📊 Quantity: {quantity}
💰 Total Price: {total_price} امتیاز"""
    
    await bot.send_message(CHANNEL_ID, message)
    await event.edit("✅ سفارش در کانال ثبت شد.", buttons=start_btn)

@bot.on(events.CallbackQuery(data="done_account_\d+_\d+"))
async def order_done_account(event):
    data = event.data.decode().split('_')
    user_id, quantity = data[1], data[2]
    
    masked_user_id = str(user_id)[:4] + "****" 
    
    message = f"""🛍 سفارش موفق استارز برای اکانت:
👤 ID: {masked_user_id}
📊 Quantity: {quantity}"""
    
    await bot.send_message(CHANNEL_ID, message)
    await event.edit("✅ سفارش در کانال ثبت شد.", buttons=start_btn)


@bot.on(events.NewMessage(pattern='🔙 بازگشت'))
async def back(event):
    await event.respond("به منوی اصلی بازگشتید ♻️", buttons=start_btn)
