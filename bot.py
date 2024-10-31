import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext, CallbackQueryHandler

TOKEN = "6414679474:AAHBrTFt5sCbbudkXHu3JvPrR_Pj50T30qs"
CHANNEL_USERNAME = "@mirali_vibe"  # نام کاربری کانال شما

# لینک‌های مخصوص فایل‌ها
file_links = {
    "seft": "Seft (Djsajjad1 & BLH Remix).mp3",
    "gang-vaghei": "Gang Vaghei (BLH Remix).mp3",
    "tamum-shode": "Pishro - Tamum Shode (featuring Kamyar).mp3"
}

# لیست کاربران عضو شده
joined_users = set()

async def send_file(user_id: int, context: CallbackContext, file_name: str):
    file_path = f"/workspaces/MyFile/{file_name}"
    await context.bot.send_document(chat_id=user_id, document=open(file_path, 'rb'))
    await context.bot.send_message(chat_id=user_id, text="فایل ارسال شد.")

async def send_join_request(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("عضویت در کانال", url="https://t.me/mirali_vibe")],
        [InlineKeyboardButton("تایید عضویت", callback_data='confirm_membership')],
        [InlineKeyboardButton("پشتیبانی", url="https://t.me/mirali_official")]  # لینک پشتیبانی
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "لطفاً به کانال ما بپیوندید و پس از عضویت دکمه زیر را فشار دهید.",
        reply_markup=reply_markup
    )

async def check_membership(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()  # پاسخ به callback query

    user_id = query.from_user.id

    try:
        # چک کردن وضعیت عضویت کاربر
        chat_member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)

        # اگر کاربر عضو کانال باشد
        if chat_member.status in ['member', 'administrator', 'creator']:
            joined_users.add(user_id)  # اضافه کردن کاربر به لیست کاربران عضو
            await query.message.reply_text("شما در کانال عضو هستید. فایل ارسال خواهد شد.")
            await send_file(user_id, context, "Pishro - Tamum Shode (featuring Kamyar).mp3")  # ارسال فایل به صورت پیش‌فرض
        else:
            await send_join_request(update, context)
    except Exception as e:
        print(f"خطا در بررسی عضویت: {str(e)}")
        await query.message.reply_text(f"خطا در بررسی عضویت: {str(e)}")

async def start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    # اگر کاربر قبلاً عضو بوده اما اکنون خارج شده است
    if user_id in joined_users:
        chat_member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)
        if chat_member.status not in ['member', 'administrator', 'creator']:
            joined_users.remove(user_id)
            await update.message.reply_text("شما از کانال خارج شده‌اید. لطفاً برای ادامه استفاده از ربات، دوباره عضو شوید.")
            await send_join_request(update, context)
            return

    # بررسی پارامتر استارت
    if context.args:
        file_key = context.args[0].lower()
        if file_key in file_links:
            await send_file(update.message.chat.id, context, file_links[file_key])
        else:
            await update.message.reply_text("فایل مورد نظر موجود نیست.")
    else:
        await update.message.reply_text("به ربات آپلودر ShadowRap خوش اومدید.\nسعی کنید نسبت به قبل تغییر زیادی نداشته باشید.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))  # هندلر برای /start
    app.add_handler(CallbackQueryHandler(check_membership, pattern='^confirm_membership$'))  # هندلر برای تایید عضویت
    app.run_polling()

if __name__ == "__main__":
    main()
