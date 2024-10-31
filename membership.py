from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from bot import send_file

CHANNEL_USERNAME = "@mirali_vibe"  # نام کاربری کانال شما

# تابع برای ارسال لینک عضویت
async def send_join_request(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("عضویت در کانال", url="https://t.me/mirali_vibe")],
        [InlineKeyboardButton("تایید عضویت", callback_data='confirm_membership')]
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
