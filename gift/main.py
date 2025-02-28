import asyncio
import sqlite3

from telethon import Button, events
from telethon.tl import functions, types

import admin
import database
from config import *


def connect_db():
    return sqlite3.connect("Gift.db")

start_btn = [
    [Button.text("لیست گیفت های موجود")],
    [Button.text("ثبت آگهی", resize=True), Button.text("ثبت درخواست")],
    [Button.text("پشتیبانی")]
]

back_btn = [
    [Button.text("برگشت", resize=True)]
]

@bot.on(events.NewMessage(pattern=r"^/start$"))
async def start(event):
    user_id = event.sender_id
    is_member = await check_membership(user_id)
    if database.is_banned(user_id):
        return
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    conn.commit()
    conn.close()
    
    if is_member :
        await event.reply("به ربات ثبت سفارش خوش آمدید! برای ثبت سفارش، کلیک کنید.", buttons=start_btn)
    else:
        await send_join_prompt(user_id, event.chat_id)

@bot.on(events.NewMessage(pattern=r"لیست گیفت های موجود"))
async def lists_gift(event):
    user_id = event.sender_id
    if database.is_banned(user_id):
        return
    await event.respond("کاربر گرامی این بخش فعلا در دسترس نیست\nدر آپدیت های بعدی اضافه خواهد شد")

@bot.on(events.NewMessage(pattern=r"^ثبت درخواست$"))
async def want_order(event):
    user_id = event.sender_id
    user = await bot.get_entity(user_id)
    username = user.username    

    is_member = await check_membership(user_id)
    if database.is_banned(user_id):
        return
    
    if is_member:
        async with bot.conversation(user_id) as conv:
            await conv.send_message("📌 لطفاً دسته‌بندی درخواست خود را وارد کنید (مثلاً: مار، ساعت، کلاه و ...)", buttons=back_btn)
            category = await conv.get_response(timeout=3600)

            if category.text == "برگشت":
                    await conv.send_message("❌ عملیات لغو شد.", buttons=start_btn)
                    return
            
            await conv.send_message("💰 لطفاً بودجه خود را بر حسب Ton وارد کنید:", buttons=back_btn)
            budget = await conv.get_response(timeout=3600)

            if budget.text == "برگشت":
                    await conv.send_message("❌ عملیات لغو شد.", buttons=start_btn)
                    return

            try:
                budget_value = float(budget.text)
                if budget_value <= 0:
                    raise ValueError
            except ValueError:
                await conv.send_message("❌ مقدار وارد شده نامعتبر است. عملیات لغو شد.")
                return
            
            await conv.send_message("📝 توضیحات مورد نیاز را وارد کنید (یا روی 'بدون توضیح' کلیک کنید):", 
                                    buttons=[[Button.text("بدون توضیح", resize=True)], [Button.text("برگشت")]])
            description = await conv.get_response(timeout=3600)

            if description.text == "برگشت":
                    await conv.send_message("❌ عملیات لغو شد.", buttons=start_btn)
                    return

            description_text = description.text if description.text != "بدون توضیح" else "بدون توضیح"
            
            conn = sqlite3.connect("Gift.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO requests (user_id, category, budget, description) VALUES (?, ?, ?, ?)",
                           (user_id, category.text, budget_value, description_text))
            conn.commit()
            request_id = cursor.lastrowid
            conn.close()

            user = await bot.get_entity(user_id)
            username = user.username
            first_name = user.first_name

            if username:
                user_mention = f"@{username}" 
            elif first_name:
                user_mention = f'<a href="tg://user?id={user_id}">{first_name}</a>'
            else :
                user_mention = f'<a href="tg://user?id={user_id}">کاربر بدون آیدی</a>'
            
            buttons = [
                [Button.inline("✅ پذیرش", f"request_accept_{request_id}".encode())],
                [Button.inline("❌ رد", f"request_reject_{request_id}".encode())],
                [Button.inline("🚫 بن", f"ban_{user_id}".encode())]
            ]
            admin_msg = f"📌 درخواست جدید دریافت شد!\n👤 کاربر: `{user_id}`\n📂 دسته‌بندی: {category.text}\n💰 بودجه: {budget_value}\n📝 توضیحات: {description_text}\n آیدی شخص ثبت کننده : {username}\nتگ آیدی : {user_mention}"
            await bot.send_message(admin_id, admin_msg, buttons=buttons, link_preview=False)
            await conv.send_message("✅ درخواست شما ارسال شد و در حال بررسی است.")
            await event.respond("به منوی اصلی بازگشتید", buttons=start_btn)
    else:
        await send_join_prompt(user_id, event.chat_id)

@bot.on(events.CallbackQuery())
async def handle_callback_requests(event):
    data = event.data.decode()

    try:
        conn = connect_db()
        cursor = conn.cursor()

        if data.startswith("request_accept_"):
            await event.answer()
            request_id = int(data.split("_")[2])
            cursor.execute("SELECT user_id, category, budget, description FROM requests WHERE id = ?", (request_id,))
            request = cursor.fetchone()

            if not request:
                await event.edit("❌ درخواست یافت نشد.")
                return
            
            user_id, category, budget, description = request
            cursor.execute("UPDATE requests SET status = 'accepted' WHERE id = ?", (request_id,))
            conn.commit()

            user = await bot.get_entity(user_id)
            username = user.username
            first_name = user.first_name

            if username:
                user_mention = f"@{username}" 
            elif first_name:
                user_mention = f'<a href="tg://user?id={user_id}">{first_name}</a>'
            else:
                user_mention = f'<a href="tg://user?id={user_id}">کاربر بدون آیدی</a>'

            channel_message = (f"📢 **درخواست جدید ثبت شد!**\n\n"
                               f"📂 دسته‌بندی: {category}\n"
                               f"💰 بودجه: {budget} TON\n"
                               f"📝 توضیحات: {description}\n"
                               f"👤 درخواست شده توسط: {user_mention}")

            await event.edit("✅ درخواست پذیرفته شد و در کانال ثبت شد!")
            await bot.send_message(user_id, "✅ درخواست شما پذیرفته شد و در کانال ثبت شد!")
            await bot.send_message(channel_id, channel_message, parse_mode="html")

        elif data.startswith("request_reject_"):
            await event.answer()
            request_id = int(data.split("_")[2])
            cursor.execute("SELECT user_id FROM requests WHERE id = ?", (request_id,))
            result = cursor.fetchone()

            if result:
                user_id = result[0]
                cursor.execute("UPDATE requests SET status = 'rejected' WHERE id = ?", (request_id,))
                conn.commit()
                await event.edit("❌ درخواست رد شد.")
                await bot.send_message(user_id, "❌ درخواست شما رد شد.")
            else:
                await event.edit("❌ درخواست یافت نشد.")

    #     elif data.startswith("ban_"):
    #         await event.answer()
    #         user_id = int(data.split("_")[1])
    #         cursor.execute("INSERT OR IGNORE INTO banned_users (user_id) VALUES (?)", (user_id,))
    #         conn.commit()
    #         await event.edit(f"🚫 کاربر `{user_id}` بن شد.")
    #         try:
    #             await bot.send_message(user_id, "🚫 شما از ربات بن شدید و دیگر نمی‌توانید از آن استفاده کنید.")
    #         except Exception:
    #             pass

    # except (sqlite3.DatabaseError, ValueError) as e:
    #     await event.answer("❌ خطایی رخ داد. لطفاً دوباره تلاش کنید.")
    #     print(f"Error: {e}")

    finally:
        conn.close()

@bot.on(events.NewMessage(pattern=r"^ثبت آگهی$"))
async def order(event):
    user_id = event.sender_id
    is_member = await check_membership(user_id)
    if database.is_banned(user_id):
        return
    
    if is_member:
        async with bot.conversation(user_id) as conv:
            await conv.send_message("🔗 لطفاً لینک گیفت NFT خود را ارسال کنید:", buttons=back_btn)
            nft_link = await conv.get_response(timeout=3600)

            if nft_link.text == "برگشت":
                    await conv.send_message("❌ عملیات لغو شد.", buttons=start_btn)
                    return
            
            if not (nft_link.text.startswith("https://t.me/nft") or nft_link.text.startswith("t.me/nft")):
                await conv.send_message("❌ لینک نامعتبر است. لطفا دقت داشته باشید که حتما لینک nft تلگرامی بفرستید.")
                return
        
            await conv.send_message("💰 لطفاً قیمت را بر پایه Ton وارد کنید:")
            price = await conv.get_response(timeout=3600)

            if price.text == "برگشت":
                    await conv.send_message("❌ عملیات لغو شد.", buttons=start_btn)
                    return
            
            try:
                price_value = float(price.text)
                if price_value <= 0:
                    raise ValueError
            except ValueError:
                await conv.send_message("❌ ورودی شما نامعتبر است. عملیات لغو شد.")
                return
        
            await conv.send_message("📝 توضیحات را وارد کنید (یا روی 'بدون توضیح' کلیک کنید):", 
                                    buttons=[[Button.text("بدون توضیح", resize=True)], [Button.text("برگشت")]])
            description = await conv.get_response(timeout=3600)

            if description.text == "برگشت":
                    await conv.send_message("❌ عملیات لغو شد.", buttons=start_btn)
                    return
            
            description_text = description.text if description.text != "بدون توضیح" else "بدون توضیح"
        
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO orders (user_id, nft_link, price, description) VALUES (?, ?, ?, ?)", 
                           (user_id, nft_link.text, price_value, description_text))
            conn.commit()
            order_id = cursor.lastrowid
            conn.close()
        
            buttons = [
                [Button.inline("✅ پذیرش", f"accept_{order_id}".encode())],
                [Button.inline("❌ رد", f"reject_{order_id}".encode())],
                [Button.inline("🚫 بن", f"ban_{user_id}".encode())]
            ]

            user = await bot.get_entity(user_id)
            username = user.username
            first_name = user.first_name

            if username:
                user_mention = f"@{username}" 
            elif first_name:
                user_mention = f'<a href="tg://user?id={user_id}">{first_name}</a>'
            else :
                user_mention = f'<a href="tg://user?id={user_id}">کاربر بدون آیدی</a>'

            admin_msg = f"📌 سفارش جدید دریافت شد!\n👤 کاربر: `{user_id}`\n🔗 لینک: {nft_link.text}\n💰 قیمت: {price_value}\n📝 توضیحات: {description_text}\nتگ آیدی : {user_mention}"
            await bot.send_message(admin_id, admin_msg, buttons=buttons, link_preview=False)
            await conv.send_message("✅ سفارش شما ارسال شد و در حال بررسی است.")
            await event.respond("به منوی اصلی بازگشتید", buttons=start_btn)
    else:
        await send_join_prompt(user_id, event.chat_id)

@bot.on(events.CallbackQuery())
async def handle_callback(event):
    data = event.data.decode()
    if data.startswith("accept_"):
        await event.answer()
        order_id = int(data.split("_")[1])
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, nft_link, price, description FROM orders WHERE id = ?", (order_id,))
        order = cursor.fetchone()
        if order:
            user_id, nft_link, price, description = order
            cursor.execute("UPDATE orders SET status = 'accepted' WHERE id = ?", (order_id,))
            conn.commit()

            user = await bot.get_entity(user_id)
            username = user.username
            first_name = user.first_name

            if username:
                user_mention = f"@{username}" 
            elif first_name:
                user_mention = f'<a href="tg://user?id={user_id}">{first_name}</a>'
            else :
                user_mention = f'<a href="tg://user?id={user_id}">کاربر بدون آیدی</a>'

            channel_message = f"📢 **سفارش جدید ثبت شد!**\n\n🔗 لینک: {nft_link}\n💰 قیمت: {price} TON\n📝 توضیحات: {description}\n👤 ثبت شده توسط: {user_mention}"

            await event.edit("✅ سفارش در کانال ثبت شد!")
            await bot.send_message(user_id, "✅ سفارش شما پذیرفته شد و در کانال ثبت شد!", reply_to=True)
            await bot.send_message(channel_id, channel_message, parse_mode="markdown")
        conn.close()
    elif data.startswith("reject_"):
        await event.answer()
        order_id = int(data.split("_")[1])
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM orders WHERE id = ?", (order_id,))
        user_id = cursor.fetchone()[0]
        cursor.execute("UPDATE orders SET status = 'rejected' WHERE id = ?", (order_id,))
        conn.commit()
        await event.edit("❌ سفارش رد شد.")
        await bot.send_message(user_id, "❌ سفارش شما رد شد.")
        conn.close()


@bot.on(events.CallbackQuery(pattern=r"^ban_(\d+)$"))
async def handle_ban(event):
    data = event.data.decode()
    user_id = int(data.split("_")[1])

    try:
        conn = connect_db()
        cursor = conn.cursor()

        # بررسی اینکه آیا کاربر قبلاً بن شده یا نه
        cursor.execute("SELECT user_id FROM banned_users WHERE user_id = ?", (user_id,))
        already_banned = cursor.fetchone()

        if already_banned:
            await event.answer("⚠ این کاربر قبلاً بن شده است.", alert=True)
            return

        # بن کردن کاربر
        cursor.execute("INSERT INTO banned_users (user_id) VALUES (?)", (user_id,))
        conn.commit()

        await event.edit(f"🚫 کاربر `{user_id}` از ربات بن شد.")

        try:
            await bot.send_message(user_id, "🚫 شما از ربات بن شدید و دیگر نمی‌توانید از آن استفاده کنید.")
        except Exception:
            pass  # کاربر ممکن است ربات را بلاک کرده باشد

    except sqlite3.DatabaseError as e:
        await event.answer("❌ خطایی رخ داد. لطفاً دوباره تلاش کنید.", alert=True)
        print(f"Database Error: {e}")

    finally:
        conn.close()

@bot.on(events.CallbackQuery(data=b'confirm_membership'))
async def confirm_membership(event):
    user_id = event.sender_id
    non_member_channels = await check_membership(user_id)

    if non_member_channels:
            
        await event.delete()
        await event.respond('✅ عضویت شما در تمام کانال‌ها تأیید شد!\nمجددا دستور مورد نظر خودتون رو بفرستید')
    else:
        await event.answer('❗ لطفاً ابتدا در تمام کانال‌ها عضو شوید و دوباره امتحان کنید.', alert=True)

async def check_membership(user_id):
    try:
        await bot(functions.channels.GetParticipantRequest(
            channel=types.PeerChannel(int(CHANNEL_ID)), 
            participant=user_id
        ))
        return True
    except Exception:
        return False 

async def send_join_prompt(user_id, chat_id):
    is_member = await check_membership(user_id)

    if is_member:
        await bot.send_message(chat_id, '✅ عضویت شما در کانال تأیید شد!')
    else:
        buttons = [
            [Button.url(f'عضویت در {CHANNEL_NAME}', url=CHANNEL_LINK)],
            [Button.inline('✅ تأیید عضویت', b'confirm_membership')]
        ]
        await bot.send_message(chat_id, '❌ لطفاً ابتدا در کانال زیر عضو شوید:', buttons=buttons)

@bot.on(events.NewMessage(pattern=r"پشتیبانی"))
async def support(event):
    user_id = event.sender_id
    if database.is_banned(user_id):
        return
    
    is_member = await check_membership(user_id)

    if is_member:
        async with bot.conversation(user_id) as conv:
            try:
                msg = await conv.send_message(
                    'شما درحال ارسال پیام به پشتیبانی هستید (توجه کنید که هیچ نوع رسانه‌ای را شما نمیتوانید ارسال کنید در نتیجه فقط متن بنویسید !)',
                    buttons=[[Button.text("برگشت", resize=True)]]
                )
                
                response = await conv.get_response(timeout=3600)

                if response.text == "برگشت":
                    await conv.send_message("❌ عملیات لغو شد.", buttons=start_btn)
                    return

                await conv.send_message("✅ پیام شما ارسال شد! لطفاً منتظر پاسخ پشتیبانی باشید.", buttons=start_btn)

                supp_btn = [
                    [Button.inline("✅ بررسی شد", data=f"checked_{user_id}")],
                    [Button.inline("❌ رد شد", data=f"rejected_{user_id}")],
                    [Button.inline("🗣 ارسال پاسخ", data=f"reply_{user_id}")]
                ]
                await bot.send_message(
                    admin_id,
                    f"📩 پیام جدید از کاربر `{user_id}`:\n\n🔹 {response.text}",
                    buttons=supp_btn
                )
            except Exception as e:
                print(f"❌ خطا در مکالمه: {e}")
                await event.respond("⚠️ مشکلی پیش آمد. لطفاً دوباره تلاش کنید.")
    else:
        await send_join_prompt(user_id, event.chat_id)

@bot.on(events.CallbackQuery(pattern=rb"checked_(\d+)"))
async def checked(event):
    user_id = int(event.pattern_match.group(1))
    await event.edit("✅ پیام بررسی شد و تأیید گردید.")
    await bot.send_message(user_id, "✅ پیام شما توسط پشتیبانی بررسی شد.")

@bot.on(events.CallbackQuery(pattern=rb"rejected_(\d+)"))
async def rejected(event):
    user_id = int(event.pattern_match.group(1))
    await event.edit("❌ پیام رد شد.")
    await bot.send_message(user_id, "❌ پیام شما رد شد.")

@bot.on(events.CallbackQuery(pattern=rb"reply_(\d+)"))
async def reply_user(event):
    user_id = int(event.pattern_match.group(1))
    async with bot.conversation(event.chat_id) as conv:
        try:
            await conv.send_message("🗣 لطفاً پیام پاسخ را وارد کنید:")
            response = await conv.get_response(timeout=3600)

            await bot.send_message(user_id, f"📩 پیام جدید از پشتیبانی:\n\n{response.text}")
            await event.respond("✅ پاسخ شما به کاربر ارسال شد.")

        except Exception as e:
            print(f"❌ خطا در پاسخ به کاربر: {e}")
            await event.respond("⚠️ مشکلی پیش آمد. لطفاً دوباره تلاش کنید.")

async def main():
    await bot.start()
    print("Connected !")
    await bot.run_until_disconnected()

if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("Disconnected !")
