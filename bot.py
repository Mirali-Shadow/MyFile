import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext, CallbackQueryHandler

# توکن بات شما
TOKEN = "6414679474:AAHBrTFt5sCbbudkXHu3JvPrR_Pj50T30qs"
CHANNEL_USERNAME = "@mirali_vibe"  # نام کاربری کانال شما
SUPPORT_CHAT_ID = "@MiRALi_OFFiCiAL"  # شناسه چت شما برای دریافت پیام‌های پشتیبانی

# تابع برای ارسال فایل
async def send_file(user_id: int, context: CallbackContext):
    file_path = "/workspaces/MyFile/Pishro - Tamum Shode (featuring Kamyar).mp3"
    await context.bot.send_document(chat_id=user_id, document=open(file_path, 'rb'))
    await context.bot.send_message(chat_id=user_id, text="فایل ارسال شد.")

# تابع برای ارسال لینک عضویت
async def send_join_request(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("عضویت در کانال", url="https://t.me/mirali_vibe")],
        [InlineKeyboardButton("تایید عضویت", callback_data='confirm_membership')],
        [InlineKeyboardButton("ارتباط با پشتیبانی", callback_data='contact_support')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "لطفاً به کانال ما بپیوندید و پس از عضویت دکمه زیر را فشار دهید.",
        reply_markup=reply_markup
    )

# تابع برای بررسی عضویت
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
        print(f"خطا در بررسی عضویت: {str(e)}")
        await query.message.reply_text(f"خطا در بررسی عضویت: {str(e)}")

# تابع برای ارتباط با پشتیبانی
async def contact_support(update: Update, context: CallbackContext) -> None:
    user_id = update.callback_query.from_user.id  # شناسه کاربر
    await context.bot.send_message(chat_id=SUPPORT_CHAT_ID, text=f"کاربر {user_id} درخواست پشتیبانی دارد.")
    await update.callback_query.answer("پیام شما به پشتیبانی ارسال شد.")

# تابع شروع
async def start(update: Update, context: CallbackContext) -> None:
    await send_join_request(update, context)

# راه‌اندازی و افزودن هندلرها
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))  # هندلر برای /start
    app.add_handler(CallbackQueryHandler(check_membership, pattern='^confirm_membership$'))  # هندلر برای تایید عضویت
    app.add_handler(CallbackQueryHandler(contact_support, pattern='^contact_support$'))  # هندلر برای تماس با پشتیبانی
    app.run_polling()

if __name__ == "__main__":
    main()
