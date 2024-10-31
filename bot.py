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
    await context.bot.send_message(chat_id=user_id, text=" فایل رو در جایی ذخیره کنید .\n فایل های ارسالی بعد از 60 ثانیه پاک خواهند شد ! ")

async def send_join_request(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("عضویت در کانال", url="https://t.me/mirali_vibe")],
        [InlineKeyboardButton("تایید عضویت", callback_data='confirm_membership')],
        [InlineKeyboardButton(" ارتباط با پشتیبانی ", url="https://t.me/mirali_official")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "لطفاً ابتدا در کانال ما عضو شوید و سپس دکمه تایید عضویت را بزنید.",
        reply_markup=reply_markup
    )

async def check_membership(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    try:
        # بررسی وضعیت عضویت کاربر
        chat_member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)

        if chat_member.status in ['member', 'administrator', 'creator']:
            joined_users.add(user_id)  # ذخیره کاربر به عنوان عضو کانال
            await query.message.reply_text("شما در کانال عضو هستید. فایل مورد نظر ارسال خواهد شد.")
        else:
            await query.message.reply_text("شما هنوز عضو کانال نیستید. لطفاً عضو شوید و دوباره امتحان کنید.")
    except Exception as e:
        print(f"خطا در بررسی عضویت: {str(e)}")
        await query.message.reply_text(f"خطا در بررسی عضویت: {str(e)}")

async def start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    # بررسی وضعیت عضویت کاربر در هر بار استارت
    try:
        chat_member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)
        if chat_member.status in ['member', 'administrator', 'creator']:
            joined_users.add(user_id)  # ذخیره کاربر به عنوان عضو کانال
            # بررسی پارامتر استارت برای ارسال فایل مورد نظر
            if context.args:
                file_key = context.args[0].lower()
                if file_key in file_links:
                    await send_file(update.message.chat.id, context, file_links[file_key])
                else:
                    await update.message.reply_text("فایل مورد نظر موجود نیست.")
            else:
                await update.message.reply_text("به ربات آپلودر ShadowRap خوش اومدید.")
        else:
            await send_join_request(update, context)
    except Exception as e:
        print(f"خطا در بررسی عضویت: {str(e)}")
        await update.message.reply_text("خطا در بررسی عضویت. لطفاً دوباره تلاش کنید.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))  # هندلر برای /start
    app.add_handler(CallbackQueryHandler(check_membership, pattern='^confirm_membership$'))  # هندلر برای تایید عضویت
    app.run_polling()

if __name__ == "__main__":
    main()
