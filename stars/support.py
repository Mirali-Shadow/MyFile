import json
from telethon import Button, events
import time
import config
import membership

chek = membership.check_membership
sj = membership.send_join_prompt
bot = config.bot
support_id = config.support_id 
QUEUE_FILE = "support_queue.json"
TIME_LIMIT = 24 * 3600


def save_queue(data):
    with open(QUEUE_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def load_queue():
    try:
        with open(QUEUE_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def add_to_queue(user_id, message_text):
    queue = load_queue()
    current_time = time.time()
    
    queue[str(user_id)] = {
        "message": message_text,
        "timestamp": current_time 
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


def can_send_message(user_id):
    queue = load_queue()
    user_data = queue.get(str(user_id))
    
    if user_data:
        last_time = user_data["timestamp"]
        if time.time() - last_time < TIME_LIMIT:
            return False 
    
    return True 


@events.register(events.NewMessage(pattern="☎️ پشتیبانی"))
async def support(event):
    user_id = event.sender_id

    start_btn = [
        [Button.text("⭐️ ثبت سفارش استارز ⭐️", resize=True, single_use=True)],
        [Button.text("👤 حساب کاربری"), Button.text("💰 افزایش موجودی")],
        [Button.text("☎️ پشتیبانی")],
        [Button.text("📖")]
    ]

    if not can_send_message(user_id):
        await event.respond("⚠️ شما فقط هر ۲۴ ساعت یکبار می‌توانید به پشتیبانی پیام دهید. لطفاً بعداً دوباره تلاش کنید.")
        return

    non_member_channels = await chek(user_id)

    if not non_member_channels:
        async with bot.conversation(user_id) as conv:
            try:
                msg = await conv.send_message(
                    '🛠 شما در حال ارسال پیام به پشتیبانی هستید.\n'
                    'لطفاً پیام خود را ارسال کنید:\n\n'
                    '🔙 برای لغو، دکمه‌ی "بازگشت" را فشار دهید.',
                    buttons=[[Button.text("🔙 بازگشت", resize=True)]]
                )
                
                response = await conv.get_response()

                if response.text == "🔙 بازگشت":
                    await conv.send_message("❌ عملیات لغو شد.")
                    await event.respond("به منوی اصلی بازگشتید", buttons=start_btn)
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
        await sj(user_id, event.chat_id)


@events.register(events.NewMessage(pattern="/admin_support"))
async def show_support_queue(event):
    if event.sender_id != support_id:
        return

    queue = load_queue()
    if not queue:
        await event.reply("✅ هیچ پیام جدیدی در صف پشتیبانی وجود ندارد.")
        return

    message = "📌 **لیست پیام‌های پشتیبانی در انتظار بررسی:**\n\n"
    for user_id, data in queue.items():
        message += f"👤 **کاربر:** `{user_id}`\n📩 **پیام:** {data['message']}\n\n"

    await bot.send_message(support_id, message)


@bot.on(events.CallbackQuery(pattern=r"checked_(\d+)"))
async def checked(event):
    user_id = int(event.pattern_match.group(1))
    await event.edit("✅ پیام بررسی شد و تأیید گردید.")
    await bot.send_message(user_id, "✅ پیام شما توسط پشتیبانی بررسی شد.")
    
    update_timestamp(user_id)
    remove_from_queue(user_id)


@bot.on(events.CallbackQuery(pattern=r"rejected_(\d+)"))
async def rejected(event):
    user_id = int(event.pattern_match.group(1))
    await event.edit("❌ پیام رد شد.")
    await bot.send_message(user_id, "❌ پیام شما به دلیل نقض قوانین رد شد.")
    
    update_timestamp(user_id)
    remove_from_queue(user_id)


@bot.on(events.CallbackQuery(pattern=r"reply_(\d+)"))
async def reply_user(event):
    user_id = int(event.pattern_match.group(1))
    async with bot.conversation(event.chat_id) as conv:
        try:
            await conv.send_message("🗣 لطفاً پیام پاسخ را وارد کنید:")
            response = await conv.get_response()

            await bot.send_message(user_id, f"📩 پیام جدید از پشتیبانی:\n\n{response.text}")
            await event.edit("✅ پاسخ شما به کاربر ارسال شد.")
            
            update_timestamp(user_id)
            remove_from_queue(user_id)
        except Exception as e:
            print(f"❌ خطا در پاسخ به کاربر: {e}")
            await event.respond("⚠️ مشکلی پیش آمد. لطفاً دوباره تلاش کنید.")
