import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext, CallbackQueryHandler, MessageHandler, filters
from collections import defaultdict

TOKEN = "7901203126:AAHdctO95WMVFgZaqdS0guzrmJURuz4tS3Q"
CHANNEL_USERNAME = "@MIRALI_VIBE"  # نام کاربری کانال

file_links = {
    "seft": "Seft (Djsajjad1 & BLH Remix).mp3",
    "gang-vaghei": "Gang Vaghei (BLH Remix).mp3",
    "tamum-shode": "Pishro - Tamum Shode (featuring Kamyar).mp3"
}

joined_users = set()
download_counts = defaultdict(int)  # برای ثبت تعداد دانلود
MAX_DOWNLOADS = 5  # محدودیت تعداد دانلود

async def send_file(user_id: int, context: CallbackContext, file_name: str):
    file_path = f"/path/to/files/{file_name}"
    if not os.path.exists(file_path):
        await context.bot.send_message(chat_id=user_id, text="فایل در دسترس نیست.")
        return
    
    if download_counts[user_id] >= MAX_DOWNLOADS:
        await context.bot.send_message(chat_id=user_id, text="شما به حد مجاز دانلود رسیدید.")
        return
    
    message = await context.bot.send_document(chat_id=user_id, document=open(file_path, 'rb'))
    message_text = await context.bot.send_message(chat_id=user_id, text="فایل را ذخیره کنید. فایل‌ها بعد از 60 ثانیه پاک می‌شوند.")
    
    download_counts[user_id] += 1  # به‌روزرسانی شمارش دانلود
    await asyncio.sleep(60)
    
    await context.bot.delete_message(chat_id=user_id, message_id=message.message_id)
    await context.bot.delete_message(chat_id=user_id, message_id=message_text.message_id)
    await context.bot.send_message(chat_id=user_id, text="⚠️ فایل حذف شد. اگر دوباره نیاز به فایل دارید، دوباره درخواست دهید.")

async def send_join_request(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("عضویت در کانال", url="https://t.me/your_channel")],
        [InlineKeyboardButton("تایید عضویت", callback_data='confirm_membership')],
        [InlineKeyboardButton("پشتیبانی", url="https://t.me/your_support")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("لطفاً ابتدا عضو کانال شوید و سپس تایید عضویت را بزنید.", reply_markup=reply_markup)

async def check_membership(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    try:
        chat_member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)
        if chat_member.status in ['member', 'administrator', 'creator']:
            joined_users.add(user_id)
            await query.message.reply_text("عضویت تایید شد. فایل مورد نظر ارسال خواهد شد.")
        else:
            await query.message.reply_text("هنوز عضو کانال نیستید. لطفاً عضو شوید.")
    except Exception as e:
        await query.message.reply_text(f"خطا در بررسی عضویت: {str(e)}")

async def list_files(update: Update, context: CallbackContext) -> None:
    file_list = "\n".join([f"/file_{key} - {key.replace('-', ' ').title()}" for key in file_links.keys()])
    await update.message.reply_text(f"لیست فایل‌های موجود:\n{file_list}")

async def start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    try:
        chat_member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)
        if chat_member.status in ['member', 'administrator', 'creator']:
            joined_users.add(user_id)
            if context.args:
                file_key = context.args[0].lower()
                if file_key in file_links:
                    await send_file(update.message.chat.id, context, file_links[file_key])
                else:
                    await update.message.reply_text("فایل مورد نظر موجود نیست.")
            else:
                await update.message.reply_text("به ربات دانلود خوش آمدید. از /help برای دریافت راهنما استفاده کنید.")
        else:
            await send_join_request(update, context)
    except Exception as e:
        await update.message.reply_text("خطا در بررسی عضویت. لطفاً دوباره تلاش کنید.")

async def feedback(update: Update, context: CallbackContext) -> None:
    feedback_text = " ".join(context.args)
    if feedback_text:
        await context.bot.send_message(chat_id="YOUR_ADMIN_CHAT_ID", text=f"بازخورد جدید از {update.message.from_user.username}: {feedback_text}")
        await update.message.reply_text("بازخورد شما دریافت شد. ممنونیم!")
    else:
        await update.message.reply_text("لطفاً بازخورد خود را پس از دستور /feedback وارد کنید.")

async def help_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "/start - شروع کار با ربات\n"
        "/list_files - نمایش لیست فایل‌ها\n"
        "/feedback - ارسال بازخورد\n"
        "/file_<نام فایل> - دریافت فایل مورد نظر\n"
    )

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("list_files", list_files))
    app.add_handler(CommandHandler("feedback", feedback))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(check_membership, pattern='^confirm_membership$'))
    app.run_polling()

if __name__ == "__main__":
    main()
