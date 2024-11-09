import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext, CallbackQueryHandler
from collections import defaultdict

TOKEN = "6414679474:AAHBrTFt5sCbbudkXHu3JvPrR_Pj50T30qs"
CHANNEL_USERNAME = "@mirali_vibe"  # نام کاربری کانال

# لینک‌های فایل‌های تست
file_links = {
    "song1": "https://www.shadowofficial.great-site.net/MyMusic/Barzakh.mp3",
    "song2": "Gang Vaghei (BLH Remix).mp3",
    "song3": "Pishro - Tamum Shode (featuring Kamyar).mp3"
}

joined_users = set()
download_counts = defaultdict(int)
MAX_DOWNLOADS = 5

# پیام شیشه‌ای با قابلیت حذف خودکار
async def send_glass_message(context: CallbackContext, user_id: int, text: str, delay: int = 60):
    message = await context.bot.send_message(chat_id=user_id, text=text)
    await asyncio.sleep(delay)
    await context.bot.delete_message(chat_id=user_id, message_id=message.message_id)

# ارسال فایل به کاربر به عنوان پیام شیشه‌ای
async def send_file_glass(user_id: int, context: CallbackContext, file_name: str):
    file_path = f"/path/to/your/files/{file_name}"
    if not os.path.exists(file_path):
        await context.bot.send_message(chat_id=user_id, text="⚠️ فایل مورد نظر موجود نیست.")
        return

    if download_counts[user_id] >= MAX_DOWNLOADS:
        await context.bot.send_message(chat_id=user_id, text="⚠️ به حد مجاز دانلود رسیدید.")
        return

    message = await context.bot.send_document(chat_id=user_id, document=open(file_path, 'rb'))
    download_counts[user_id] += 1
    await asyncio.sleep(60)
    await context.bot.delete_message(chat_id=user_id, message_id=message.message_id)
    await context.bot.send_message(chat_id=user_id, text="فایل به طور خودکار حذف شد. دوباره درخواست دهید.")

# درخواست عضویت در کانال با تاییدیه
async def send_join_request(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("عضویت در کانال", url="https://t.me/your_channel")],
        [InlineKeyboardButton("تایید عضویت", callback_data='confirm_membership')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("لطفاً عضو کانال شوید و سپس تایید عضویت را بزنید.", reply_markup=reply_markup)

# بررسی عضویت کاربر
async def check_membership(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    try:
        chat_member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)
        if chat_member.status in ['member', 'administrator', 'creator']:
            joined_users.add(user_id)
            await send_glass_message(context, user_id, "✅ عضویت تایید شد.", delay=10)
        else:
            await query.message.reply_text("❌ هنوز عضو نیستید.")
    except Exception as e:
        await query.message.reply_text("❌ خطا در بررسی عضویت.")

# نمایش لیست فایل‌ها
async def list_files(update: Update, context: CallbackContext) -> None:
    file_list = "\n".join([f"/file_{key} - {key.replace('-', ' ').title()}" for key in file_links.keys()])
    await update.message.reply_text(f"لیست فایل‌های موجود:\n{file_list}")

# دستور /start با پیام شیشه‌ای
async def start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    try:
        chat_member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)
        if chat_member.status in ['member', 'administrator', 'creator']:
            joined_users.add(user_id)
            await send_glass_message(context, user_id, "به ربات خوش آمدید! از /help برای دریافت راهنما استفاده کنید.")
        else:
            await send_join_request(update, context)
    except Exception as e:
        await update.message.reply_text("خطا در بررسی عضویت.")

# راهنما
async def help_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "دستورات ربات:\n"
        "/start - شروع ربات\n"
        "/list_files - مشاهده فایل‌ها\n"
        "/help - راهنما"
    )

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("list_files", list_files))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(check_membership, pattern='^confirm_membership$'))
    app.run_polling()

if __name__ == "__main__":
    main()
