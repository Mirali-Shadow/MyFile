import asyncio
import json
import re
import sqlite3
import time
from asyncio import sleep
from datetime import UTC, datetime

import jdatetime
import requests
from telethon import Button, events
from telethon.tl import functions, types
from telethon.tl.custom.message import Message
from telethon.tl.functions.messages import SendReactionRequest
from telethon.tl.types import InputMediaDice, ReactionEmoji, ReactionPaid

import config
import database

bot = config.bot
owner_id = config.owner_id
bot_name = config.bot_name
OWNER_ID = config.owner_id 
support_id = config.support_id 

TRANSFER_FEE = 5 
trx_point = 340

TRON_WALLET = "TDV6xMP95tjFaMHU4c9938XTCNCk33A2Kx"

QUEUE_FILE = "support_queue.json"
LAST_MESSAGE_FILE = "last_message.json"

TIME_LIMIT = 24 * 3600
CHANNEL_ID = -1002498118094 
STARS = 20 

file_id = None

start_btn = [
        [Button.text("⭐️ ثبت سفارش استارز ⭐️", resize=True, single_use=True)],
        [Button.text("👤 حساب کاربری"), Button.text("💰 مدیریت مالی")],
        [Button.text("📒 راهنما"), Button.text("🎛 سایر خدمات فرعی")],
        [Button.text("☎️ پشتیبانی")]
    ]

async def check_membership(user_id):
    all_channels = database.get_channels_from_db()
    non_member_channels = []
    
    for channel in all_channels:
        try:
            result = await bot(functions.channels.GetParticipantRequest(
                channel=types.PeerChannel(int(channel[1])), 
                participant=user_id
            ))
        except Exception:
            non_member_channels.append(channel)

    return non_member_channels

async def send_join_prompt(user_id, chat_id):
    non_member_channels = await check_membership(user_id)

    if not non_member_channels:
        await bot.send_message(chat_id, 'عضویت شما در تمام کانال‌ها تأیید شد!')
        return

    buttons = [[Button.url(f'عضویت در {channel[2]}', url=channel[0])] for channel in non_member_channels]
    buttons.append([Button.inline('تأیید عضویت ✅', b'confirm_membership')])
    await bot.send_message(chat_id, '💎 لطفاً ابتدا در کانال‌های زیر عضو شوید:', buttons=buttons)

@bot.on(events.NewMessage(pattern=r"/start"))
async def start(event):
    user_id = event.sender_id
    non_member_channels = await check_membership(user_id)
    message_text = event.message.text
    sender_name = event.sender.first_name or "NoName"

    # 📌 مقداردهی جدید برای `formatted_date` در لحظه اجرای تابع
    now = jdatetime.datetime.now()
    formatted_date = now.strftime("%Y/%m/%d - %H:%M:%S")
    
    match = re.search(r'/start (\d+)', message_text)
    inviter_id = int(match.group(1)) if match and int(match.group(1)) != user_id else None

    # ✅ بررسی اینکه کاربر از قبل در دیتابیس هست یا نه
    is_new_user = not database.user_exists(user_id)

    if not non_member_channels:
        database.add_user(user_id, inviter_id)

        # ✅ فقط اگر کاربر جدید بود، به `inviter_id` پیام بده
        if inviter_id and is_new_user:
            await bot.send_message(inviter_id, "🎉 تبریک ! یک کاربر با لینک شما ثبت نام کرد 🎁", buttons=start_btn)

        await bot.send_message(event.chat_id, f""" کاربر <b><a href='tg://user?id={user_id}'>{sender_name}</a></b> عزیز به جــت اسـتارز خوش اومدی 🏵

{formatted_date} 🕗
""", buttons=start_btn, parse_mode="html")
    else:
        if inviter_id:
            database.store_temp_inviter(user_id, inviter_id)
        await send_join_prompt(user_id, event.chat_id)

@bot.on(events.NewMessage(pattern="/help"))
async def helper(event: Message):
    user_id = event.sender_id
    if user_id == owner_id :
        await event.respond("پنل مدیریتی شما :", buttons=[[Button.text("/admin", resize=True)], [Button.text("/support")]])
    elif user_id == support_id :
        await event.respond("پنل مدیریتی شما : ", buttons=[[Button.text("/support")]])
    else :
        await event.respond("""🎉 راهنمای استفاده از ربات جت استارز  ⭐️
سلام دوست عزیز! 👋 خوش اومدی به [جت استارز] 🤖💫
با استفاده از این ربات می‌تونی استارز تلگرام دریافت کنی و از اون‌ها برای امکانات ویژه استفاده کنی! 🚀

📌 چطور استارز بگیرم؟
1️⃣ لینک اختصاصی خودتو دریافت کن!
با زدن دکمه "افزایش موجودی" لینک اختصاصی خودت رو دریافت کن.

2️⃣ دوستاتو دعوت کن!
لینک رو برای دوستانت بفرست و اون‌ها رو به ربات دعوت کن.

3️⃣ استارز هدیه بگیر! 🎁
وقتی دوستت با لینک تو وارد ربات بشه و عضو کانال‌های مورد نیاز بشه، به تو  امتیاز داده می‌شه! 🎊

4️⃣ نرخ ارزون !
قیمت هر استارز 20 امتیازه و تو میتونی به راحتی استارز خریداری کنی 
(در ضمن به این علت قیمت استارز روی اکانت 1000 امتیازه چون برای اکانت کمتر از 50 استارز نمیشه فعال کرد)

❓ سوالات متداول
❓ از کجا بفهمم چند نفر دعوت کردم؟
🔹 با زدن دکمه "حساب کاربری" می‌تونی تعداد رفرال‌های خودت و مقدار استارزت رو ببینی.
""")

@bot.on(events.CallbackQuery(data=b'confirm_membership'))
async def confirm_membership(event):
    user_id = event.sender_id
    non_member_channels = await check_membership(user_id)

    if not non_member_channels:
        inviter_id = database.get_temp_inviter(user_id)

        if inviter_id:
            if not database.is_user_registered(user_id):
                database.add_user(user_id, inviter_id) 
                await bot.send_message(inviter_id, "🎉 تبریک ! یک کاربر با لینک شما ثبت نام کرد 🎁", buttons=start_btn)
                database.remove_temp_inviter(user_id) 
            
        await event.delete()
        await event.respond('✅ عضویت شما در تمام کانال‌ها تأیید شد!\nمجددا دستور مورد نظر خودتون رو بفرستید')
    else:
        await event.answer('❗ لطفاً ابتدا در تمام کانال‌ها عضو شوید و دوباره امتحان کنید.', alert=True)

@bot.on(events.NewMessage(pattern=r"💰 مدیریت مالی"))
async def main_order(event):
    user_id = event.sender_id
    non_member_channels = await check_membership(user_id)
    
    btns = [
        [Button.text("🎮 جوایز روزانه", resize=True)],
        [Button.text("💸 انتقال امتیاز"), Button.text("➕ افزایش موجودی")],
        [Button.text("🔙 بازگشت")]
    ]
    if not non_member_channels:
        await event.respond("💰 به بخش مدیریت مالی خوش اومدید ⭐️", buttons=btns)
    else:
        await send_join_prompt(user_id, event.chat_id)

@bot.on(events.NewMessage(pattern=r"🎮 جوایز روزانه"))
async def daily_gifts(event):
    user_id = event.sender_id
    non_member_channels = await check_membership(user_id)
    
    btn = [
        [Button.text("🎲 تاس", resize=True)],
        [Button.text("🔙 بازگشت به منوی قبل", single_use=True)]
    ]
    if not non_member_channels:
        await event.respond("به بخش جوایز روزانه خوش اومدید \n\nاز منوی زیر گزینه مورد نظر خودتون رو انتخاب کنید", buttons=btn)
    else:
        await send_join_prompt(user_id, event.chat_id)

@bot.on(events.NewMessage(pattern=r"➕ افزایش موجودی"))
async def increase_orders(event):
    user_id = event.sender_id
    non_member_channels = await check_membership(user_id)
    
    btn = [
        [Button.text("🎁 شارژ از طریق رفرال", resize=True), Button.text("💷 شارژ از طریق ترون")],
        [Button.text("💳 شارژ تومان")],
        [Button.text("🏷 ارسال توکن جت استارز")],
        [Button.text("🔙 بازگشت به منوی قبل")]
    ]
    if not non_member_channels:
        await event.respond(f"""به بخش افزایش موجودی خوش اومدید

🔸 در این بخش شما میتونید به روش دلخواه خودتون حسابتون رو شارژ کنید 
🔸 به ازای هر 1 ترون به شما {trx_point} امتیاز تعلق خواهد گرفت
🔸 به ازای هر 1 رفرال به شما `10` امتیاز تعلق خواهد گرفت
""", buttons=btn)
    else:
        await send_join_prompt(user_id, event.chat_id)

@bot.on(events.NewMessage(pattern=r"💷 شارژ از طریق ترون"))
async def increase_order_trx(event):
    user_id = event.sender_id
    non_member_channels = await check_membership(user_id)
    
    btn = [
        [Button.inline("ادامه ✅", b"confirm_deposit")],
        [Button.inline("بازگشت", b"back_to_order")]
    ]
    if not non_member_channels:
        await event.respond(f"""🔒 شرایط و ضوابط استفاده :

1️⃣ پرداخت های زیر 1 ترون تایید نمیشود .

2️⃣ از انتقال مقدار غیر رند جدا خودداری فرمایید . ( برای مثال مقدار واریزی 2.6 ترون ، فقط 2 ترون آن قابل پذیرش است)

3️⃣ هر ترون برابر `{trx_point}` امتیاز میباشد .

4️⃣ شارژ حساب شما به صورت آنی و خودکار انجام میشود .
""", buttons=btn)
    else:
        await send_join_prompt(user_id, event.chat_id)

@bot.on(events.NewMessage(pattern=r"💳 شارژ تومان"))
async def buy_toman(event):
    user_id = event.sender_id
    non_member_channels = await check_membership(user_id)
    if not non_member_channels:
        await event.respond("""🔰 کاربر گرامی فعلا امکان ایجاد درگاه پرداخت وجود ندارد
به همین علت شما میتوانید از طریق ارتباط با آیدی @Jet_Ad حساب خود را شارژ نمایید 🌹
""")
    else:
        await send_join_prompt(user_id, event.chat_id)

@bot.on(events.NewMessage(pattern=r"🏷 ارسال توکن جت استارز"))
async def jet_token(event: Message):
    user_id = event.sender_id
    non_member_channels = await check_membership(user_id)
    if not non_member_channels:
        await event.respond("""کاربر گرامی این بخش در آپدیت های بعدی اضافه خواهد شد 
از شکیبایی شما سپاسگذاریم 💎
""")
    else:
        await send_join_prompt(user_id, event.chat_id)

@bot.on(events.NewMessage(pattern=r"💸 انتقال امتیاز"))
async def transfer_order(event):
    user_id = event.sender_id
    non_member_channels = await check_membership(user_id)
    
    btn = [
        [Button.inline("ادامه ✅", b"transfer_point")],
        [Button.inline("بازگشت", b"back_to_order")]
    ]
    if not non_member_channels: 
        await event.respond(f"""🟡 برای انتقال امتیاز شما باید حتما آیدی عددی کاربری که قصد دارید برای او امتیاز بفرستید را داشته باشید ! 
                        
<blockquote>- اگر آیدی عددی کاربر را ندارید میتوانید از بخش "سایر خدمات فرعی" > "گرفتن آیدی عددی" آیدی عددی شخص مورد نظر خود را دریافت کنید</blockquote>

🔸 همچنین برای انتقال امتیاز مجموعه مقدار <code>{TRANSFER_FEE}</code> امتیاز را به عنوان کارمزد در نظر گرفته است که موجودی شما میبایست از این مقدار بیشتر باشد ✅

درصورت پذیرش شرایط بالا بر روی ادامه کلیک کنید 💎
""", buttons=btn, parse_mode="html")
    else:
        await send_join_prompt(user_id, event.chat_id)

@bot.on(events.CallbackQuery(data=b"transfer_point"))
async def start_transfer(event):
    user_id = event.sender_id
    
    await event.delete()
    
    async with bot.conversation(user_id) as conv:
        cancel_button = [[Button.text("❌ انصراف", resize=True, single_use=True)]]
        
        await conv.send_message("👤 آیدی عددی گیرنده را ارسال کنید:", buttons=cancel_button)
        response = await conv.get_response()
        if response.text == "❌ انصراف":
            await conv.send_message("🚫 عملیات انتقال لغو شد.", buttons=start_btn)
            return
        
        try:
            receiver_id = int(response.text)
        except ValueError:
            await conv.send_message("⚠️ لطفاً یک آیدی عددی معتبر ارسال کنید!", buttons=start_btn)
            return
        
        if not database.user_exists_t(receiver_id):
            await conv.send_message("❌ کاربر موردنظر یافت نشد!", buttons=start_btn)
            return
        
        await conv.send_message("💰 مقدار امتیازی که می‌خواهید انتقال دهید را ارسال کنید:", buttons=cancel_button)
        response = await conv.get_response()
        if response.text == "❌ انصراف":
            await conv.send_message("🚫 عملیات انتقال لغو شد.", buttons=start_btn)
            return
        
        try:
            amount = int(response.text)
            if amount <= TRANSFER_FEE:
                await conv.send_message(f"⚠️ مقدار امتیاز باید بیشتر از {TRANSFER_FEE} باشد!", buttons=start_btn)
                return
        except ValueError:
            await conv.send_message("⚠️ لطفاً یک مقدار معتبر ارسال کنید!", buttons=start_btn)
            return
        
        user_balance = database.get_user_points_t(user_id)

        if user_balance < amount:
            await conv.send_message(f"❌ موجودی شما کافی نیست!\n💰 موجودی شما: {user_balance} امتیاز", buttons=start_btn)
            return
        
        final_amount = amount - TRANSFER_FEE  # مقدار نهایی که گیرنده دریافت می‌کند

        confirm_buttons = [
            [Button.inline("✅ تایید", data=f"confirm_transfer_{user_id}_{receiver_id}_{amount}")],
            [Button.inline("❌ لغو", data="cancel_transfer")]
        ]
        
        await conv.send_message(
            f"🎯 **انتقال امتیاز**\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"👤 **گیرنده:** `{receiver_id}`\n"
            f"💎 **مقدار انتقال:** `{amount}` امتیاز\n"
            f"💰 **کارمزد:** `{TRANSFER_FEE}` امتیاز\n"
            f"📥 **دریافتی نهایی:** `{amount - TRANSFER_FEE}` امتیاز\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "✅ **آیا این انتقال را تأیید می‌کنید؟**",
            buttons=confirm_buttons
        )

@bot.on(events.CallbackQuery(pattern=r"confirm_transfer_(\d+)_(\d+)_(\d+)"))
async def confirm_transfer(event):
    match = event.pattern_match.groups()
    sender_id = int(match[0])
    receiver_id = int(match[1])
    amount = int(match[2])
    
    user_balance = database.get_user_points_t(sender_id)

    if user_balance < amount:
        await event.answer("❌ موجودی شما کافی نیست!", alert=True)
        return
    
    final_amount = amount - TRANSFER_FEE  # مقدار نهایی که گیرنده دریافت می‌کند

    # ✅ کاهش موجودی فرستنده و اضافه کردن به گیرنده
    database.update_user_points_t(sender_id, user_balance - amount)
    database.update_user_points_t(receiver_id, database.get_user_points_t(receiver_id) + final_amount)
    
    await event.edit("✅ انتقال با موفقیت انجام شد!")
    await bot.send_message(
        sender_id,
        f"✅ انتقال موفقیت‌آمیز بود!\n👤 گیرنده: `{receiver_id}`\n💰 مقدار ارسال شده: {amount} امتیاز\n⚡️ کارمزد: {TRANSFER_FEE} امتیاز\n📥 مقدار دریافتی گیرنده: {final_amount} امتیاز",
        buttons=start_btn
    )

    # اطلاع‌رسانی به گیرنده
    await bot.send_message(receiver_id, f"🎁 شما `{final_amount}` امتیاز از کاربر `{sender_id}` دریافت کردید!", buttons=start_btn)

@bot.on(events.CallbackQuery(pattern=r"cancel_transfer"))
async def cancel_transfer(event):
    await event.edit("🚫 عملیات انتقال لغو شد.")

        # ثبت تراکنش در دیتابیس
        # database.record_transaction_t(f"transfer_{user_id}_{receiver_id}_{time.time()}", user_id, -total_amount)
        # database.record_transaction_t(f"transfer_{receiver_id}_{user_id}_{time.time()}", receiver_id, amount)

@bot.on(events.CallbackQuery(data=b"back_to_order"))
async def back_to_order(event):
    await event.delete()
    await main_order(event)

@bot.on(events.NewMessage(pattern=r"🔙 بازگشت به منوی قبل"))
async def back_to_order(event):
    user_id = event.sender_id
    non_member_channels = await check_membership(user_id)
    if not non_member_channels:
        await main_order(event)
    else:
        await send_join_prompt(user_id, event.chat_id)

@bot.on(events.NewMessage(pattern=r"👤 حساب کاربری"))
async def account(event):
    user_id = event.sender_id
    non_member_channels = await check_membership(user_id)
    
    user_info = database.get_full_user_info(user_id)
    transaction_count = database.get_user_transaction_count_trx(user_id)
    
    if not user_info:
        await bot.send_message(event.chat_id, "❌ شما هنوز ثبت‌نام نکرده‌اید!\nبرای ثبت نام کافیه کلمه /start رو بفرستید")
        return

    points, referrals = user_info[1], user_info[2]
    
    account_text = (
        f"📊 **اطلاعات حساب کاربری شما** 📊\n\n"
        f"🧩 شناسه عددی : `{user_id}`\n"
        f"🏅 **امتیاز:** `{points}`\n"
        f"👥 **تعداد رفرال‌ها:** `{referrals}`\n"
        f"🔹 تعداد تراکنش های انجام شده : `{transaction_count}`"
    )
    if not non_member_channels:
        await bot.send_message(event.chat_id, account_text)
    else:
        await send_join_prompt(user_id, event.chat_id)

@bot.on(events.NewMessage(pattern=r'⭐️ ثبت سفارش استارز ⭐️'))
async def stars(event):
    user_id = event.sender_id
    non_member_channels = await check_membership(user_id)
    
    btn = [
        [Button.text("استارز برای پست 🌟"), Button.text("استارز برای اکانت ✴️")],
        [Button.text("🔙 بازگشت", resize=True)]
    ]
    if not non_member_channels:
        await bot.send_message(event.chat_id, """🔶 کاربر گرامی به بخش سفارش استارز خوش اومدید 

♦️ قیمت هر استارز برابر با 20 امتیاز میباشد !
♦️ توجه: حداقل امتیاز برای سفارش استارز برای اکانت 1000 امتیاز است ❗️ 
(چون برای اکانت سفارشات کمتر از 50 استارز قابل انجام نیست)

⚠️🚨 توجه اگر شما در قسمت لینک ، به جز لینک چیز دیگه ای نوشتید سفارش شما توسط بات پردازش نمیشه و امتیاز شما سوخت خواهد شد 🚨⚠️
""", buttons=btn)
    else:
        await send_join_prompt(user_id, event.chat_id)

@bot.on(events.NewMessage(pattern="استارز برای پست 🌟"))
async def stars_for_post(event):
    user_id = event.sender_id
    user_points = database.get_user_points(user_id)
    sender_name = event.sender.first_name or "کاربر"
    non_member_channels = await check_membership(user_id)

    if not non_member_channels : 

        async with bot.conversation(event.chat_id) as conv:
            buttons = [[Button.text("🔙 بازگشت", resize=True)]]
            await conv.send_message("لطفاً مقدار استارز مورد نیاز خودتون رو بنویسید", buttons=buttons)
            response1 = await conv.get_response(timeout=3600)
        
            if response1.text == "🔙 بازگشت":
                await conv.send_message("🚫 عملیات سفارش استارز لغو شد.", buttons=start_btn)
                return

            try:
                quantity = int(response1.text)
                if quantity <= 0:
                    await conv.send_message("❌ مقدار وارد شده نامعتبر است!")
                    return
            except ValueError:
                await conv.send_message("❌ لطفاً یک عدد معتبر وارد کنید!")
                return

            await conv.send_message("لطفاً لینک پست مورد نظر را ارسال کنید")
            response2 = await conv.get_response(timeout=3600)
            post_link = response2.text
        
            if response2.text == "🔙 بازگشت":
                await conv.send_message("🚫 عملیات سفارش استارز لغو شد.", buttons=start_btn)
                return

            total_price = quantity * STARS

            if user_points < total_price:
                await conv.send_message("❌ امتیاز شما کافی نیست!", buttons=start_btn)
                return

            database.decrease_user_points_for_order(user_id, total_price)
            database.add_order(user_id, "استارز روی پست", quantity, total_price, post_link)

            buttons = [
                [Button.url("مشاهده پست", post_link)],
                [Button.inline("✅ انجام شد", data=f"done_{user_id}_{quantity}_{total_price}")]
            ]

            await bot.send_message(
                OWNER_ID, 
                f"📢 سفارش جدید استارز:\n\\🗣 acc : <b><a href='tg://user?id={user_id}'>{sender_name}</a></\nnnnn👤 ID: {user_id}\n📊 Quantity: {quantity}\n💰 Total Price: {total_price} امتیاز", 
                buttons=buttons,
                parse_mode="html"
            )
            await conv.send_message("✅ سفارش شما ثبت شد و در حال پردازش است.", buttons=start_btn)

    else :
        await send_join_prompt(user_id, event.chat_id)

@bot.on(events.NewMessage(pattern="استارز برای اکانت ✴️"))
async def stars_for_account(event):
    user_id = event.sender_id
    user_points = database.get_user_points(user_id)
    sender_name = event.sender.first_name or "کاربر"
    non_member_channels = await check_membership(user_id)

    if not non_member_channels:

        if user_points < 1000:
            await bot.send_message(event.chat_id, "❌ امتیاز شما کافی نیست! حداقل 1000 امتیاز نیاز دارید.")
            return

        user_can = user_points // 20

        async with bot.conversation(event.chat_id) as conv:
            buttons = [[Button.text("🔙 بازگشت", resize=True)]]
            await conv.send_message(f"شما {user_points} امتیاز دارید. مقدار مورد نظر خود را (بین 50 تا {user_can}) وارد کنید:", buttons=buttons)
            response1 = await conv.get_response(timeout=3600)
        
            if response1.text == "🔙 بازگشت":
                await conv.send_message("🚫 عملیات سفارش استارز لغو شد.", buttons=start_btn)
                return

            try:
                quantity = int(response1.text)
                if quantity < 50 or quantity > user_points:
                    await conv.send_message("❌ مقدار وارد شده نامعتبر است!")
                    return
            except ValueError:
                await conv.send_message("❌ لطفاً یک عدد معتبر وارد کنید!")
                return

            await conv.send_message("لطفاً یوزرنیم اکانت خود را با @ وارد کنید:")
            response2 = await conv.get_response(timeout=3600)
            username = response2.text
        
            if response2.text == "🔙 بازگشت":
                await conv.send_message("🚫 عملیات سفارش استارز لغو شد.", buttons=start_btn)
                return
            
            quantity_to_decrease = quantity * 20

            database.decrease_user_points_for_order(user_id, quantity_to_decrease)
            database.add_order(user_id, "استارز برای اکانت", quantity, quantity_to_decrease, username)

            buttons = [
                [Button.inline("✅ انجام شد", data=f"done_account_{user_id}_{quantity}")]
            ]

            await bot.send_message(
                OWNER_ID, 
                f"📢 سفارش جدید استارز برای اکانت:\n🗣 acc : <b><a href='tg://user?id={user_id}'>{sender_name}</a></b>\nsnn👤 ID: {user_id}\n📊 Quantity: {quantity}\n🔗 Username: {username}", 
                buttons=buttons,
                parse_mode="html"
            )
            await conv.send_message("✅ سفارش شما ثبت شد و در حال پردازش است.", buttons=start_btn)
    else:
        non_member_channels = await check_membership(user_id)

channels_btn = [
    [Button.url("ثبت سفارش استارز ⭐️", "https://t.me/JetStars_bot")]
]

@bot.on(events.CallbackQuery(pattern=rb"done_\d+_\d+_\d+"))
async def order_done(event):
    data = event.data.decode().split('_')
    user_id, quantity, total_price = int(data[1]), int(data[2]), int(data[3])  # تبدیل به عدد صحیح
    
    masked_user_id = str(user_id)[:4] + "****" 
    
    message = f"""🛍 سفارش موفق استارز بر روی پست:
👤 ID: {masked_user_id}
📊 Quantity: {quantity}
💰 Total Price: {total_price} امتیاز"""
    
    await bot.send_message(user_id, "سفارش شما با موفقیت انجام شد ✅", buttons=start_btn)
    await bot.send_message(CHANNEL_ID, message, buttons=channels_btn)
    await event.edit("✅ سفارش در کانال ثبت شد.", buttons=start_btn)

@bot.on(events.CallbackQuery(pattern=rb"done_account_\d+_\d+"))
async def order_done_account(event):
    data = event.data.decode().split('_')

    if len(data) < 4: 
        await event.answer("❌ خطا در پردازش داده‌ها!", alert=True)
        return
    
    user_id, quantity = int(data[2]), int(data[3])

    masked_user_id = str(user_id)
    if len(masked_user_id) > 4:
        masked_user_id = masked_user_id[:4] + "****"  
    else:
        masked_user_id = "****" 

    message = f"""🛍 سفارش موفق استارز برای اکانت:
👤 ID: {masked_user_id}
📊 Quantity: {quantity}"""
    
    await bot.send_message(user_id, "سفارش شما با موفقیت انجام شد ✅", buttons=start_btn)
    await bot.send_message(CHANNEL_ID, message, buttons=channels_btn)
    await event.edit("✅ سفارش در کانال ثبت شد.", buttons=start_btn)

@bot.on(events.NewMessage(pattern='^🔙 بازگشت$'))
async def back(event):
    user_id = event.sender_id
    non_member_channels = await check_membership(user_id)
    if not non_member_channels:
        await event.respond("به منوی اصلی بازگشتید ♻️", buttons=start_btn)
    else:
        await send_join_prompt(user_id, event.chat_id)

admin_btn = [
    [Button.inline('➕ اضافه کردن کانال', b'add_channel'), Button.inline('❌ حذف کانال', b'delete_channel')],
    [Button.inline('📋 لیست کانال‌ها', b'list_channels')],
    [Button.inline("➕ افزایش امتیاز", b"increase_points"), Button.inline("➖ کاهش امتیاز", b"decrease_points")],
    [Button.inline("📋 لیست همه کاربران", b"all_list")],
    [Button.inline("🔍 بررسی کاربر", b"check_user")],
    [Button.inline("تغییر امتیاز همگانی 🎁", b"modify_points")],
    [Button.inline("🔊 پیام همگانی", b"broadcast")],
    [Button.inline("❌ بستن پنل", b"close_panel")]
]

@bot.on(events.NewMessage(pattern=r"/admin"))
async def admin_panel(event):
    user_id = event.sender_id
    if user_id == owner_id:
        await event.respond("🎛 پنل مدیریت باز شد:", buttons=admin_btn)

@bot.on(events.CallbackQuery(data="modify_points"))
async def modify_user_points(event):
    await event.answer()

    btn = [
        [Button.text("لغو", resize=True)]
    ]


    async with bot.conversation(event.sender_id) as conv:
        await conv.send_message("⏳ لطفاً مقدار امتیاز را وارد کنید یا 'لغو' را ارسال کنید:", buttons=btn)

        while True:
            response = await conv.get_response(timeout=3600)
            if response.text.lower() == "لغو":
                await event.delete()
                await event.respond("❌ عملیات لغو شد.")
                await admin_panel(event)
                return

            try:
                points = int(response.text)
                break
            except ValueError:
                await conv.send_message("⚠️ لطفاً فقط یک عدد صحیح ارسال کنید:")

    database.update_all_users_points(points)
    
    users = database.get_all_users_for_all()
    for user in users:
        try:
            await bot.send_message(user, f"🎁 {points} امتیاز از طرف ادمین به حساب شما اضافه شد!" if points > 0 else f"❌ {abs(points)} امتیاز از حساب شما کم شد!")
        except Exception:
            pass 

    await event.respond(f"✅ {points} امتیاز برای همه کاربران اعمال شد!")

@bot.on(events.CallbackQuery(data=b'add_channel'))
async def add_channel(event):
    await event.respond('لطفاً لینک نمایشی کانال را ارسال کنید:')
    
    @bot.on(events.NewMessage(from_users=owner_id))
    async def get_display_link(e):
        display_link = e.text
        await e.respond('نام نمایشی کانال را وارد کنید:')

        @bot.on(events.NewMessage(from_users=owner_id))
        async def get_display_name(e2):
            display_name = e2.text
            await e2.respond('حالا یک پیام از کانال مورد نظر را فوروارد کنید یا آی‌دی عددی کانال را ارسال کنید:')

            @bot.on(events.NewMessage(from_users=owner_id))
            async def get_channel_id(e3):
                if e3.forward:
                    channel_id = e3.forward.chat.id
                else:
                    try:
                        channel_id = int(e3.text)
                    except ValueError:
                        await e3.respond('آی‌دی کانال نامعتبر است. عملیات لغو شد.')
                        return
                
                database.add_channel_to_db(display_link, channel_id, display_name)
                await e3.respond('کانال با موفقیت اضافه شد!')
                bot.remove_event_handler(get_channel_id)
            bot.remove_event_handler(get_display_name)
        bot.remove_event_handler(get_display_link)

@bot.on(events.CallbackQuery(data=b'delete_channel'))
async def delete_channel(event):
    channels = database.get_all_channels()
    if not channels:
        await event.respond('هیچ کانالی برای حذف وجود ندارد.')
        return

    buttons = [[Button.inline(channel[1], f"del_{str(channel[0])}")] for channel in channels]
    buttons.append([Button.inline("بازگشت به پنل ادمین", b"back_to_admin")])  # اصلاح آرایه دکمه‌ها

    await event.edit('کانال مورد نظر را انتخاب کنید:', buttons=buttons)

@bot.on(events.CallbackQuery(pattern=b'del_'))
async def confirm_delete(event):
    channel_id = int(event.data.decode().split('_')[1])
    database.delete_channel_from_db(channel_id)
    await event.respond('کانال با موفقیت حذف شد!')

@bot.on(events.CallbackQuery(data=b'list_channels'))
async def list_channels(event):
    channels = database.get_channels_list()
    if not channels:
        await event.respond('هیچ کانالی تعریف نشده است.')
    else:
        channel_list = '\n'.join([f'- نام : {c[0]}\n لینک: {c[1]}\n, آی‌دی: {c[2]}\n' for c in channels])
        await event.respond(f'لیست کانال‌ها:\n{channel_list}', link_preview=False)

@bot.on(events.CallbackQuery(data=b"back_to_admin"))
async def back_to_admin(event):
    await event.delete()
    await admin_panel(event)

@bot.on(events.CallbackQuery(data=b"all_list"))
async def show_all_users(event):
    users = database.get_all_users()
    if not users:
        await event.answer("❌ هیچ کاربری یافت نشد!", alert=True)
        return

    messages = []
    message = "📋 **لیست کاربران:**\n\n"

    for index, user in enumerate(users, start=1):
        line = f"{index}. 👤 **User ID:** `{user[0]}` | ⭐️ point: `{user[1]}` | 👥 invited: `{user[2]}`\n"

        if message.count("\n") < 25:  # اگر تعداد خطوط کمتر از 25 است، اضافه کند
            message += line
        else:  # در غیر این صورت، پیام فعلی را ذخیره کرده و یک پیام جدید شروع کند
            messages.append(message)
            message = line

    if message:  # اگر متنی باقی مانده باشد، به لیست پیام‌ها اضافه شود
        messages.append(message)

    for msg in messages:  # ارسال هر پیام جداگانه
        await event.respond(msg)

@bot.on(events.CallbackQuery(data=b"check_user"))
async def ask_user_id(event):
    async with bot.conversation(event.sender_id) as conv:
        # ✅ ارسال پیام به صورت مکالمه
        await conv.send_message("🔎 لطفاً **آیدی عددی کاربر** را ارسال کنید:")

        # ✅ دریافت پاسخ کاربر
        response = await conv.get_response(timeout=3600)

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
        
        response = await conv.get_response(timeout=3600)
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
        
        response = await conv.get_response(timeout=3600)
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
            message = await conv.get_response(timeout=3600)
        
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

@bot.on(events.CallbackQuery(data=b"close_panel"))
async def close_panel(event):
    await event.edit("✅ پنل مدیریت بسته شد.", buttons=[Button.inline("باز کردن پنل", b"back_to_panel")])

@bot.on(events.CallbackQuery(data=b"back_to_panel"))
async def back_to_panel(event):
    await event.delete()
    await admin_panel(event)

# @bot.on(events.NewMessage(pattern=r'💰 افزایش موجودی'))
# async def increase(event):
#     user_id = event.sender_id
#     message_text = event.message.text
#     non_member_channels = await check_membership(user_id)

#     btn = [
#         [Button.text("🎁 شارژ از طریق رفرال", resize=True), Button.text("🎮 جایزه روزانه")],
#         [Button.text("↩️ بازگشت")]
#     ]

#     if not non_member_channels:
#         await event.respond(f"به بخش شارژ حساب کاربری خوش اومدید خوش آمدید!🎉 \nتو این بخش میتونید با انتخاب گزینه مورد نظرتون حساب خودتون رو شارژ کنید", buttons=btn)
#     else:
#         await send_join_prompt(user_id, event.chat_id)

file_id = None
last_upload_time = 0 
UPLOAD_INTERVAL = 3600 

async def upload_photo_once():
    """فقط اگر از آخرین آپلود بیش از 1 ساعت گذشته باشد، دوباره آپلود می‌کند"""
    global file_id, last_upload_time

    now = time.time() 
    if file_id is None or (now - last_upload_time) > UPLOAD_INTERVAL:
        file_id = await bot.upload_file("photo.png")
        last_upload_time = now 
        print("✅ فایل دوباره آپلود شد!")
    
    return file_id

@bot.on(events.NewMessage(pattern=r"🎁 شارژ از طریق رفرال"))
async def buy_order(event):
    user_id = event.sender_id
    referral_link = f"https://t.me/{bot_name}?start={user_id}"
    
    non_member_channels = await check_membership(user_id)

    if not non_member_channels:
        file = await upload_photo_once()
        
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
        await event.respond("""برای دریافت استارز از طریق رفرال ، پیام بالا رو منتشر کنید.

هر کاربری که با استفاده از لینک شما وارد ربات شود ، به شما 10 سکه تعلق می‌گیرد.
""")
        
    else:
        await send_join_prompt(user_id, event.chat_id)

@bot.on(events.NewMessage(pattern=r"↩️ بازگشت"))
async def come_back(event: Message):
    user_id = event.sender_id
    non_member_channels = await check_membership(user_id)
    if not non_member_channels:
        await event.respond("به منوی اصلی بازگشتید ♻️", buttons=start_btn)
    else:
        await send_join_prompt(user_id, event.chat_id)

@bot.on(events.CallbackQuery(data=b"confirm_deposit"))
async def confirm_deposit(event):
    await event.delete()
    async with bot.conversation(event.sender_id) as conv:
        await conv.send_message(f"🪙 لطفاً مقدار ترون را به این آدرس واریز کنید:\n`{TRON_WALLET}`\n\nسپس لینک تراکنش را ارسال کنید.\n\n⚠️🚨 توجه ، اگر لینک تراکنش را ارسال نکنید و واریز کرده باشید تحت هیچ شرایطی امتیازی به شما تعلق نخواهد گرفت 🚨⚠️")
        tx_link = await conv.get_response(timeout=3600)
        
        tx_id = tx_link.text.split("/")[-1]
        
        if database.is_transaction_exists_trx(tx_id):
            await conv.send_message("🚨 خطا: این تراکنش قبلاً ثبت شده است! شما اخطار دریافت کردید!")
            return
        
        is_valid, amount, tx_data = check_transaction(tx_id)
        if not is_valid or amount <= 0:
            await conv.send_message("❌ تراکنش نامعتبر است یا به ولت درستی واریز نشده!")
            return
        
        points_to_add = int(amount * trx_point)
        user_id = event.sender_id
        database.update_user_points_trx(user_id, database.get_user_points_trx(user_id) + points_to_add)
        
        database.add_transaction_trx(tx_id, user_id, amount)
        
        await conv.send_message(f"✅ تراکنش تأیید شد! {points_to_add} امتیاز به حساب شما اضافه شد.")
        await bot.forward_messages(owner_id, tx_link)
        
        message = f"""🆕 تراکنش جدید ثبت شد!  
👤 کاربر: `{user_id}`  
📌 وضعیت: SUCCESS  
💰 مقدار: {amount} TRX  
⏳ زمان تراکنش: {tx_data['timestamp']}  
🔄 از: `{tx_data['from_address']}`  
➡️ به: `{tx_data['to_address']}`  
🔗 هش: `{tx_id}`  
        """
        await bot.send_message(owner_id, message)

def check_transaction(tx_id):
    url = f"https://apilist.tronscan.org/api/transaction-info?hash={tx_id}"
    response = requests.get(url)
    
    if response.status_code != 200:
        return False, 0, None
    
    data = response.json()
    
    if "contractData" not in data or "owner_address" not in data["contractData"] or "to_address" not in data["contractData"]:
        return False, 0, None
    
    from_address = data["contractData"]["owner_address"]
    to_address = data["contractData"]["to_address"].lower()
    amount = data["contractData"].get("amount", 0) / 1e6
    timestamp = data.get("timestamp")
    if timestamp:
        timestamp = datetime.fromtimestamp(timestamp / 1000, UTC).strftime('%Y-%m-%d %H:%M:%S')
    else:
        timestamp = "نامشخص"
    
    if to_address != TRON_WALLET.lower() or amount < 1:
        return False, 0, None
    
    tx_data = {
        "from_address": from_address,
        "to_address": to_address,
        "timestamp": timestamp
    }
    
    return True, amount, tx_data

@bot.on(events.NewMessage(pattern=r"🎲 تاس"))
async def daily(event):
    user_id = event.sender_id
    non_member_channel = await check_membership(user_id)
    
    btn = [
        [Button.inline("🎲 انداختن تاس ✅", b"send_dice")], 
        [Button.inline("🔙 بازگشت", b"back_to_menu")]
    ]
    
    if not non_member_channel: 

        if database.get_referral_count(user_id) >= 5:
            if database.can_claim_reward(user_id):
                await event.respond(
                    "🔰 کاربر گرامی به بخش جایزه روزانه خوش اومدید 😇\n"
                    "شما از طریق این بخش میتونید هر 24 ساعت یکبار، شانس خودتون رو برای دریافت امتیاز امتحان کنید ⭐️",
                    buttons=btn
                )
            else:
                await event.respond("❌ شما امروز جایزه روزانه را دریافت کرده‌اید! لطفاً ۲۴ ساعت صبر کنید.")
        else:
            await event.respond("👤 برای شرکت در بخش جایزه روزانه باید حداقل ۵ نفر را دعوت کرده باشید ‼️")
    else: 
        await send_join_prompt(user_id, event.chat_id)


@bot.on(events.CallbackQuery(data=b"send_dice"))
async def dice_callback(event):
    user_id = event.sender_id

    if not database.can_claim_reward(user_id):
        await event.edit("❌ شما امروز جایزه روزانه را دریافت کرده‌اید! لطفاً ۲۴ ساعت صبر کنید.")
        return

    await event.edit("🎲 منتظر نتیجه باشید ...")
    dice = await bot.send_file(event.chat_id, file=InputMediaDice(emoticon="🎲"))
    value = dice.dice.value

    database.add_points(user_id, value)
    database.update_last_claim(user_id)
    
    await sleep(2)
    await bot.send_message(event.chat_id, f"🎉 شما {value} امتیاز دریافت کردید!")

@bot.on(events.CallbackQuery(data=b"back_to_menu"))
async def back_to_menu(event):
    await event.delete()
    await event.respond("به منوی قبل بازگشتید ♻️")

#___________________ jsons_create  ________________________
# def create_json_files(file1, file2):
#     data = {"message": "This is a sample JSON file."}

#     with open(file1, "w", encoding="utf-8") as f1:
#         json.dump(data, f1, ensure_ascii=False, indent=4)

#     with open(file2, "w", encoding="utf-8") as f2:
#         json.dump(data, f2, ensure_ascii=False, indent=4)

#     print(f"✅ دو فایل {file1} و {file2} ایجاد شدند.")

# file_name1 = "last_message.json"
# file_name2 = "support_queue.json"

# create_json_files(file_name1, file_name2)
#_________________________________________________

@bot.on(events.NewMessage(pattern=r"📒 راهنما"))
async def helper(event):
    user_id = event.chat_id
    
    non_member_channels = await check_membership(user_id)
    
    if not non_member_channels :
        await event.respond("""🎉 راهنمای استفاده از ربات جت استارز  ⭐️
سلام دوست عزیز! 👋 خوش اومدی به [جت استارز] 🤖💫
با استفاده از این ربات می‌تونی استارز تلگرام دریافت کنی و از اون‌ها برای امکانات ویژه استفاده کنی! 🚀

📌 چطور استارز بگیرم؟
1️⃣ لینک اختصاصی خودتو دریافت کن!
با زدن دکمه "افزایش موجودی" لینک اختصاصی خودت رو دریافت کن.

2️⃣ دوستاتو دعوت کن!
لینک رو برای دوستانت بفرست و اون‌ها رو به ربات دعوت کن.

3️⃣ استارز هدیه بگیر! 🎁
وقتی دوستت با لینک تو وارد ربات بشه و عضو کانال‌های مورد نیاز بشه، به تو  امتیاز داده می‌شه! 🎊

4️⃣ نرخ ارزون !
قیمت هر استارز 20 امتیازه و تو میتونی به راحتی استارز خریداری کنی 
(در ضمن به این علت قیمت استارز روی اکانت 1000 امتیازه چون برای اکانت کمتر از 50 استارز نمیشه فعال کرد)

❓ سوالات متداول
❓ از کجا بفهمم چند نفر دعوت کردم؟
🔹 با زدن دکمه "حساب کاربری" می‌تونی تعداد رفرال‌های خودت و مقدار استارزت رو ببینی.
""")
    else :
        await send_join_prompt(user_id, event.chat_id)

#_________________Jsons______________________

def save_queue(data):
    with open(QUEUE_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def load_queue():
    try:
        with open(QUEUE_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading queue: {e}")
        return {}

def save_last_message(data):
    with open(LAST_MESSAGE_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def load_last_message():
    try:
        with open(LAST_MESSAGE_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def update_last_message(user_id):
    last_messages = load_last_message()
    last_messages[str(user_id)] = time.time()  # ذخیره زمان ارسال پیام
    save_last_message(last_messages)

def can_send_message(user_id):
    last_messages = load_last_message()
    last_time = last_messages.get(str(user_id)) or 0

    if last_time and time.time() - last_time < TIME_LIMIT:
        return False  # هنوز ۲۴ ساعت نگذشته
    return True  # می‌تواند پیام جدید ارسال کند

def add_to_queue(user_id, message_text):
    queue = load_queue()
    if not isinstance(queue, dict):  # اطمینان از اینکه داده‌ها یک دیکشنری هستند
        queue = {}

    queue[str(user_id)] = {
        "message": message_text,
        "timestamp": time.time()
    }
    save_queue(queue)

def remove_from_queue(user_id):
    queue = load_queue()
    if str(user_id) in queue:
        del queue[str(user_id)]
        save_queue(queue)

def update_timestamp(user_id):
    queue = load_queue()
    current_time = time.time()
    
    if str(user_id) in queue:
        queue[str(user_id)]["timestamp"] = current_time
    
    save_queue(queue)

@bot.on(events.NewMessage(pattern=r"/support"))
async def supp(event):
    if event.sender_id not in [support_id, owner_id]:
        return
    
    btn = [
        [Button.inline("لیست پیام های پشتیبانی 🗒", b"support_list")],
        [Button.inline("💬 پیام به یک کاربر 👤", b"message_fast")]
    ]
    
    await bot.send_message(event.chat_id, "درود پشتیبان عزیز ، به پنل خودتون خوش اومدید", buttons=btn)

@bot.on(events.CallbackQuery(pattern=rb"support_list"))
async def show_support_queue(event):

    queue = load_queue()
    if not isinstance(queue, dict):  # بررسی اینکه queue دیکشنری است
        await event.reply("❌ خطا در بارگذاری پیام‌ها. لطفاً بررسی کنید که داده‌ها به‌درستی ذخیره شده‌اند.")
        return

    if not queue:
        await event.reply("✅ هیچ پیام جدیدی در صف پشتیبانی وجود ندارد.")
        return

    await event.reply("📌 **لیست پیام‌های پشتیبانی در انتظار بررسی:**\n\n")

    for user_id, data in queue.items():
        if isinstance(data, dict) and 'message' in data:
            msg_text = f"👤 **کاربر:** `{user_id}`\n📩 **پیام:** {data['message']}"

            buttons = [
                [Button.inline("✅ بررسی شد", data=f"checked_{user_id}")],
                [Button.inline("❌ رد شد", data=f"rejected_{user_id}")],
                [Button.inline("🗣 ارسال پاسخ", data=f"reply_{user_id}")]
            ]

            await bot.send_message(event.sender_id, msg_text, buttons=buttons)
        else:
            await event.reply(f"⚠️ داده‌های نادرستی برای کاربر `{user_id}` پیدا شد.")

@bot.on(events.CallbackQuery(pattern=rb"checked_(\d+)"))
async def checked(event):
    user_id = int(event.pattern_match.group(1))
    await event.edit("✅ پیام بررسی شد و تأیید گردید.")
    await bot.send_message(user_id, "✅ پیام شما توسط پشتیبانی بررسی شد.")

    update_last_message(user_id) 
    remove_from_queue(user_id)

@bot.on(events.CallbackQuery(pattern=rb"rejected_(\d+)"))
async def rejected(event):
    user_id = int(event.pattern_match.group(1))
    await event.edit("❌ پیام رد شد.")
    await bot.send_message(user_id, "❌ پیام شما به دلیل نقض قوانین رد شد.")

    update_last_message(user_id)
    remove_from_queue(user_id) 

@bot.on(events.CallbackQuery(pattern=rb"reply_(\d+)"))
async def reply_user(event):
    user_id = int(event.pattern_match.group(1))
    async with bot.conversation(event.chat_id) as conv:
        try:
            await conv.send_message("🗣 لطفاً پیام پاسخ را وارد کنید:")
            response = await conv.get_response(timeout=3600)

            await bot.send_message(user_id, f"📩 پیام جدید از پشتیبانی:\n\n{response.text}")
            await event.respond("✅ پاسخ شما به کاربر ارسال شد.")

            update_last_message(user_id) 
            remove_from_queue(user_id) 
        except Exception as e:
            print(f"❌ خطا در پاسخ به کاربر: {e}")
            await event.respond("⚠️ مشکلی پیش آمد. لطفاً دوباره تلاش کنید.")

@bot.on(events.CallbackQuery(pattern=r"message_fast"))
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

@bot.on(events.NewMessage(pattern=r"☎️ پشتیبانی"))
async def support(event):
    user_id = event.sender_id

    if not can_send_message(user_id):
        await event.respond("⚠️ شما فقط هر ۲۴ ساعت یکبار می‌توانید به پشتیبانی پیام دهید. لطفاً بعداً دوباره تلاش کنید.")
        return

    non_member_channels = await check_membership(user_id)

    if not non_member_channels:
        async with bot.conversation(user_id) as conv:
            try:
                msg = await conv.send_message(
                    '🛠 شما در حال ارسال پیام به پشتیبانی هستید.\n'
                    'لطفاً پیام خود را ارسال کنید:\n\n'
                    '🔙 برای لغو، دکمه‌ی "بازگشت" را فشار دهید.',
                    buttons=[[Button.text("🔙 بازگشت", resize=True)]]
                )
                
                response = await conv.get_response(timeout=3600)

                if response.text == "🔙 بازگشت":
                    await conv.send_message("❌ عملیات لغو شد.")
                    return

                add_to_queue(user_id, response.text)

                await conv.send_message("✅ پیام شما ارسال شد! لطفاً منتظر پاسخ پشتیبانی باشید.", buttons=start_btn)

                supp_btn = [
                    [Button.inline("✅ بررسی شد", data=f"checked_{user_id}")],
                    [Button.inline("❌ رد شد", data=f"rejected_{user_id}")],
                    [Button.inline("🗣 ارسال پاسخ", data=f"reply_{user_id}")]
                ]
                await bot.send_message(
                    support_id,
                    f"📩 پیام جدید از کاربر `{user_id}`:\n\n🔹 {response.text}",
                    buttons=supp_btn
                )
            except Exception as e:
                print(f"❌ خطا در مکالمه: {e}")
                await event.respond("⚠️ مشکلی پیش آمد. لطفاً دوباره تلاش کنید.")
    else:
        await send_join_prompt(user_id, event.chat_id)

@bot.on(events.NewMessage(pattern=r"🎛 سایر خدمات فرعی"))
async def other_thing(event):
    user_id = event.sender_id
    non_member_channels = await check_membership(user_id)
    
    btn = [
        [Button.text("👤 دریافت آیدی عددی", resize=True)],
        [Button.text("🔙 بازگشت")]
    ]
    if not non_member_channels:
        await event.respond("🌀 به بخش خدمات غیر استارزی ما خوش اومدید از منوی زیر گزینه‌ای که لازم دارید رو انتخاب کنید 💯", buttons=btn)
    else:
        await send_join_prompt(user_id, event.chat_id)

@bot.on(events.NewMessage(pattern=r"👤 دریافت آیدی عددی"))
async def get_id(event):
    user_id = event.sender_id
    non_member_channels = await check_membership(user_id)
    if not non_member_channels:
        user_id = event.sender_id
        async with bot.conversation(user_id) as conv:
            cancel_btn = [Button.text("❌ انصراف", resize=True, single_use=True)]
            await conv.send_message(
                "برای دریافت آیدی عددی هر شخص، یکی از کارهای زیر را انجام دهید:\n"
                "1️⃣ یک پیام از او فوروارد کنید.\n"
                "2️⃣ یوزرنیم او را (بدون @) ارسال کنید.",
                buttons=cancel_btn
            )

            response = await conv.get_response(timeout=3600)

            if response.text == "❌ انصراف":
                await conv.send_message("✅ عملیات لغو شد.", buttons=start_btn)
                return

            if response.forward and response.forward.sender_id:
                target_id = response.forward.sender_id
                await conv.send_message(f"🔹 آیدی عددی این شخص: `{target_id}`", parse_mode="markdown", buttons=[[Button.text("👤 دریافت آیدی عددی", resize=True)], [Button.text("🔙 بازگشت")]])
                return

            username = response.text.lstrip("@") 
            try:
                entity = await bot.get_entity(username)
                target_id = entity.id
                await conv.send_message(f"🔹 آیدی عددی این شخص: `{target_id}`", parse_mode="markdown", buttons=[[Button.text("👤 دریافت آیدی عددی", resize=True)], [Button.text("🔙 بازگشت")]])
            except ValueError:
                await conv.send_message("❌ یوزرنیم نامعتبر است یا کاربر یافت نشد.", buttons=[[Button.text("👤 دریافت آیدی عددی", resize=True)], [Button.text("🔙 بازگشت")]])
    else:
        await send_join_prompt(user_id, event.chat_id)

loop = asyncio.get_event_loop()
print("bot is run ..")
loop.run_forever()