import asyncio
import re
import sqlite3
from asyncio import sleep

from telethon import Button, events
from telethon.tl import functions, types
from telethon.tl.functions.messages import SendReactionRequest
from telethon.tl.types import ReactionEmoji, ReactionPaid

import stars
import admin
import config
import database
import order
import support
import membership
import order
import user

bot = config.bot

#____________________ support _____________________
with bot as mirali :
    mirali.add_event_handler(support.support)

#___________________ admin ________________________
with bot as mirali :
    mirali.add_event_handler(admin.admin_panel)

#___________________ order ________________________
with bot as mirali :
    mirali.add_event_handler(order.increase)

#___________________ user ________________________
with bot as mirali :
    mirali.add_event_handler(user.account)

#___________________ stars ________________________
with bot as mirali :
    mirali.add_event_handler(stars.stars)


@bot.on(events.NewMessage(pattern=r"/start"))
async def start(event):
    user_id = event.sender_id
    non_member_channels = await membership.check_membership(user_id)
    message_text = event.message.text
    
    btn = [
        [Button.text("⭐️ ثبت سفارش استارز ⭐️", resize=True, single_use=True)],
        [Button.text("👤 حساب کاربری"), Button.text("💰 افزایش موجودی")],
        [Button.text("☎️ پشتیبانی")],
        [Button.text("📖")]
    ]
    
    match = re.search(r'/start (\d+)', message_text)
    inviter_id = int(match.group(1)) if match and int(match.group(1)) != user_id else None

    if not non_member_channels:
        database.add_user(user_id, inviter_id)

        if inviter_id:
            try:
                await bot.send_message(inviter_id, "🎉 تبریک ! یک کاربر با لینک شما ثبت نام کرد 🎁", buttons=btn)
            except Exception as e:
                print(f"⚠️ خطا در ارسال پیام به معرف: {e}")

        await bot.send_message(event.chat_id, "درود به ربات استارز گیر رایگان خوش اومدید", buttons=btn)
    else:
        if inviter_id:
            database.store_temp_inviter(user_id, inviter_id)
        await membership.send_join_prompt(user_id, event.chat_id)

@bot.on(events.CallbackQuery(data=b'confirm_membership'))
async def confirm_membership(event):
    user_id = event.sender_id
    non_member_channels = await membership.check_membership(user_id)

    if not non_member_channels:
        inviter_id = database.get_temp_inviter(user_id)

        if inviter_id:
            if not database.is_user_registered(user_id):
                database.add_user(user_id, inviter_id) 
                database.remove_temp_inviter(user_id) 
            
        await event.delete()
        await event.respond('✅ عضویت شما در تمام کانال‌ها تأیید شد!\nمجددا دستور مورد نظر خودتون رو بفرستید')
    else:
        await event.answer('❗ لطفاً ابتدا در تمام کانال‌ها عضو شوید و دوباره امتحان کنید.', alert=True)


loop = asyncio.get_event_loop()
bot.start()
print("run")
loop.run_forever()