import asyncio
import sqlite3

from telethon import Button, events

import database
from config import *


def connect_db():
    return sqlite3.connect("Gift.db")

@bot.on(events.NewMessage(pattern=r"^/admin$"))
async def admin_panel(event):
    if event.sender_id != admin_id:
        return
    
    buttons = [
        [Button.inline("🚫 مدیریت کاربران بن شده", b"manage_bans")],
        [Button.inline("📢 ارسال همگانی", b"send_broadcast")],
        [Button.inline("پیام به کاربر", b"message_fast")],
        [Button.inline("لیست همه کاربران", b"all_list")]
    ]
    await event.reply("🔧خوش اومدید به پنل مدیریت :", buttons=buttons)

@bot.on(events.CallbackQuery(data=b"manage_bans"))
async def manage_bans(event):
    buttons = [
        [Button.inline("👀 لیست کاربران بن شده", b"list_banned")],
        [Button.inline("➕ بن کردن کاربر", b"ban_user")],
        [Button.inline("➕ آنبن کردن کاربر", b"unban_user")],
        [Button.inline("🔙 بازگشت", b"admin_panel")]
    ]
    await event.edit("🚫 مدیریت کاربران بن شده:", buttons=buttons)

@bot.on(events.CallbackQuery(data=b"message_fast"))
async def send_custom_message(event):

    async with bot.conversation(event.sender_id) as conv:
        try:
            await conv.send_message("📌 لطفاً آیدی عددی کاربر را وارد کنید:")
            user_id_msg = await conv.get_response(timeout=3600)
            
            if not user_id_msg.text.isdigit():
                return await conv.send_message("⚠️ آیدی عددی معتبر نیست. عملیات لغو شد.")
            
            user_id = int(user_id_msg.text)

            await conv.send_message("✉️ لطفاً متن پیامی که می‌خواهید ارسال کنید را وارد نمایید:")
            message_text = await conv.get_response(timeout=3600)

            await bot.send_message(user_id, f"📩 پیام جدید از پشتیبانی:\n\n{message_text.text}")
            await conv.send_message("✅ پیام شما با موفقیت به کاربر ارسال شد.")

        except Exception as e:
            print(f"❌ خطا در ارسال پیام به کاربر {user_id}: {e}")
            await event.reply("⚠️ مشکلی پیش آمد. لطفاً دوباره تلاش کنید.")

@bot.on(events.CallbackQuery(data=b"admin_panel"))
async def admin_panel_again(event):
    await event.answer()
    await event.delete()
    await admin_panel(event)

@bot.on(events.CallbackQuery(data=b"list_banned"))
async def list_banned(event):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM banned_users")
    banned_users = cursor.fetchall()
    conn.close()
    
    if not banned_users:
        await event.answer("❌ هیچ کاربری بن نشده است!", alert=True)
        return
    
    message = "🚫 **لیست کاربران بن شده:**\n\n"
    for index, user in enumerate(banned_users, start=1):
        message += f"{index}. 👤 User ID: `{user[0]}`\n"
    
    await event.answer()
    await event.respond(message)

@bot.on(events.CallbackQuery(data=b"ban_user"))
async def ban_user(event):
    await event.answer()
    async with bot.conversation(event.sender_id) as conv:
        await conv.send_message("لطفاً آیدی عددی کاربر را برای بن کردن ارسال کنید:")
        user_id = await conv.get_response(timeout=3600)
        
        if not user_id.text.isdigit():
            await conv.send_message("❌ ورودی نامعتبر است. عملیات لغو شد.")
            return
        
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO banned_users (user_id) VALUES (?)", (int(user_id.text),))
        conn.commit()
        conn.close()
        
        await conv.send_message(f"✅ کاربر با آیدی `{user_id.text}` بن شد!")

@bot.on(events.CallbackQuery(data=b"unban_user"))
async def unban_user(event):
    await event.answer()
    async with bot.conversation(event.sender_id) as conv:
        await conv.send_message("لطفاً آیدی عددی کاربر را برای آنبن کردن ارسال کنید:")
        user_id = await conv.get_response(timeout=3600)
        
        if not user_id.text.isdigit():
            await conv.send_message("❌ ورودی نامعتبر است. عملیات لغو شد.")
            return
        
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM banned_users WHERE user_id = ?", (int(user_id.text),))
        conn.commit()
        conn.close()
        
        await conv.send_message(f"✅ کاربر با آیدی `{user_id.text}` آنبن شد!")

@bot.on(events.CallbackQuery(data=b"send_broadcast"))
async def send_broadcast(event):
    async with bot.conversation(event.sender_id) as conv:
        await conv.send_message("📢 لطفاً پیام مورد نظر را ارسال کنید:")
        message = await conv.get_response(timeout=3600)
        
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM users WHERE user_id NOT IN (SELECT user_id FROM banned_users)")
        users = cursor.fetchall()
        conn.close()
        
        for user in users:
            try:
                await bot.send_message(user[0], message.text)
            except:
                pass
        
        await conv.send_message("✅ پیام همگانی ارسال شد!")

@bot.on(events.CallbackQuery(data=b"all_list"))
async def show_all_users(event):
    users = database.get_all_users()
    if not users:
        await event.answer("❌ هیچ کاربری یافت نشد!", alert=True)
        return

    messages = []
    message = "📋 **لیست کاربران:**\n\n"

    for index, user in enumerate(users, start=1):
        line = f"{index}. 👤 **ID:** `{user[0]}`\n"

        if message.count("\n") < 25: 
            message += line
        else: 
            messages.append(message)
            message = line

    if message: 
        messages.append(message)

    for msg in messages: 
        await event.respond(msg)
