from telethon import Button, events

import config
import database
from config import owner_id

bot = config.bot

admin_btn = [
    [Button.inline("📋 لیست همه کاربران", b"all_list")],
    [Button.inline("➕ افزایش امتیاز", b"increase_points"), Button.inline("➖ کاهش امتیاز", b"decrease_points")],
    [Button.inline("🔍 بررسی کاربر", b"check_user")],
    [Button.inline("🔊 پیام همگانی", b"broadcast")],
    [Button.inline("❌ بستن پنل", b"close_panel")]
]

@events.register(events.NewMessage(pattern=r"/admin"))
async def admin_panel(event):
    user_id = event.sender_id
    if user_id == owner_id:
        await event.respond("🎛 پنل مدیریت باز شد:", buttons=admin_btn)

@bot.on(events.CallbackQuery(data=b"all_list"))
async def show_all_users(event):
    users = database.get_all_users()
    if not users:
        await event.answer("❌ هیچ کاربری یافت نشد!", alert=True)
        return

    message = "📋 **لیست کاربران:**\n\n"
    for index, user in enumerate(users, start=1):
        message += f"{index}. 👤 **User ID:** `{user[0]}` | ⭐️ point: `{user[1]}` | 👥 invited: `{user[2]}`\n"
    
    await event.respond(message)

@bot.on(events.CallbackQuery(data=b"check_user"))
async def ask_user_id(event):
    async with bot.conversation(event.sender_id) as conv:
        # ✅ ارسال پیام به صورت مکالمه
        await conv.send_message("🔎 لطفاً **آیدی عددی کاربر** را ارسال کنید:")

        # ✅ دریافت پاسخ کاربر
        response = await conv.get_response()

        user_id = response.text.strip()

        if not user_id.isdigit():
            await conv.send_message("❌ لطفاً یک آیدی عددی معتبر ارسال کنید!")
            return

        user_info = database.get_user_info(int(user_id))
        if user_info:
            await conv.send_message(f"👤 **User ID:** `{user_id}`\n⭐️ امتیاز: `{user_info[0]}`\n👥 دعوتی‌ها: `{user_info[1]}`")
        else:
            await conv.send_message("❌ کاربر یافت نشد!")

@bot.on(events.CallbackQuery(data=b"increase_points"))
async def ask_user_for_increase(event):

    async with bot.conversation(event.sender_id) as conv:
        await conv.send_message("🔢 لطفاً **آیدی عددی کاربر** و مقدار امتیاز را ارسال کنید.\n📌 فرمت: `USER_ID AMOUNT`")
        
        response = await conv.get_response()
        try:
            user_id, points = map(int, response.text.split())
            database.update_user_points(user_id, points)
            await event.respond(f"✅ {points} امتیاز به کاربر `{user_id}` اضافه شد!")
        except:
            await event.respond("❌ فرمت ورودی نادرست است! مثال: `123456789 50`")

@bot.on(events.CallbackQuery(data=b"decrease_points"))
async def ask_user_for_decrease(event):

    async with bot.conversation(event.sender_id) as conv:
        await conv.send_message("🔢 لطفاً **آیدی عددی کاربر** و مقدار امتیاز را ارسال کنید.\n📌 فرمت: `USER_ID AMOUNT`")
        
        response = await conv.get_response()
        try:
            user_id, points = map(int, response.text.split())
            database.update_user_points(user_id, -points)
            await event.respond(f"✅ {points} امتیاز از کاربر `{user_id}` کم شد!")
        except:
            await event.respond("❌ فرمت ورودی نادرست است! مثال: `123456789 50`")

@bot.on(events.CallbackQuery(data=b"broadcast"))
async def broadcast(event):
    buttons = [
        [Button.inline("📢 همگانی بات", data="broadcast_bot")],
        [Button.inline("🔄 همگانی فوروارد", data="broadcast_forward")],
        [Button.inline("بازگشت", b"back_to_panel")]
    ]
    await event.edit("لطفاً نوع ارسال پیام را انتخاب کنید:", buttons=buttons)

@bot.on(events.CallbackQuery)
async def broadcast_choice(event):
    if event.data in [b"broadcast_bot", b"broadcast_forward"]:
        is_forward = event.data == b"broadcast_forward"
        
        async with bot.conversation(event.sender_id) as conv:
            await conv.send_message("📢 لطفاً پیام موردنظر را ارسال کنید:")
            message = await conv.get_response()
        
        users = database.get_all_users_public() 
        total_users = len(users)
        count = 0

        status_msg = await event.respond(f"⏳ ارسال پیام: 0/{total_users}")

        for user in users:
            try:
                if is_forward:
                    await bot.forward_messages(user, message)
                else:
                    if message.media:
                        await bot.send_file(user, message.media, caption=message.text)
                    else:
                        await bot.send_message(user, message.text)
                
                count += 1
                if count % 10 == 0 or count == total_users:
                    await status_msg.edit(f"📊 ارسال پیام: {count}/{total_users} انجام شد")
            except:
                pass 

        await status_msg.edit("✅ پیام همگانی ارسال شد!")

@bot.on(events.CallbackQuery(data=b"back_to_panel"))
async def back_to_panel(event):
    await event.edit("🎛 پنل مدیریت باز شد:", buttons=admin_btn)

@bot.on(events.CallbackQuery(data=b"close_panel"))
async def close_panel(event):
    await event.edit("✅ پنل مدیریت بسته شد.", buttons=[Button.inline("باز کردن پنل", b"back_to_panel")])

@bot.on(events.CallbackQuery(data=b"back_to_panel"))
async def back_to_panel(event):
    await event.delete()
    await admin_panel(event)
