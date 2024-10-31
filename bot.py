import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext, MessageHandler, filters, CallbackQueryHandler

# توکن بات شما
TOKEN = "6414679474:AAHBrTFt5sCbbudkXHu3JvPrR_Pj50T30qs"
CHANNEL_USERNAME = "@mirali_vibe"  # نام کاربری کانال شما را در اینجا قرار دهید

# تابع برای ارسال پیام خوش آمدگویی
async def start(update: Update, context: CallbackContext) -> None:
    keyboard = [[
        InlineKeyboardButton("عضویت در کانال", url=f"https://t.me/{CHANNEL_USERNAME}"),
        InlineKeyboardButton("تأیید عضویت", callback_data="confirm_membership")
    ]]
    
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "لطفاً به کانال ما بپیوندید و سپس تأیید عضویت خود را کلیک کنید.",
        reply_markup=reply_markup
    )

# تابع برای بررسی عضویت کاربر در کانال
async def check_membership(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()  # پاسخ به callback query

    user_id = query.from_user.id  # شناسه کاربر
    try:
        chat_member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)
        
        if chat_member.status in ['member', 'administrator', 'creator']:
            await query.message.reply_text("شما در کانال عضو هستید. فایل ارسال خواهد شد.")
            await send_file(user_id, context)  # ارسال فایل
        else:
            await query.message.reply_text("شما در کانال عضو نیستید. لطفاً ابتدا عضو شوید.")
    except Exception as e:
        await query.message.reply_text(f"خطا در بررسی عضویت: {str(e)}")  # پیام خطا در صورت بروز مشکل

# تابع برای ارسال فایل
async def send_file(user_id: int, context: CallbackContext):
    file_path = "/workspaces/MyFile/Gang Vaghei (BLH Remix).mp3"  # مسیر فایل شما
    await context.bot.send_document(chat_id=user_id, document=open(file_path, 'rb'))

# راه‌اندازی و افزودن هندلرها
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))  # هندلر برای /start
    app.add_handler(CallbackQueryHandler(check_membership, pattern="confirm_membership"))  # هندلر برای callback query
    app.run_polling()

if __name__ == "__main__":
    main()
