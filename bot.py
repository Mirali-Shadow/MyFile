from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# مسیر فایل مورد نظر (مطمئن شوید که فایل در همان دایرکتوری وجود دارد یا مسیر کامل آن را بنویسید)
FILE_PATH = "https://github.com/MIRALILOR/MyFile/blob/d19550a1a44891fc9dff7f485d80df17e60f0412/MyMusic/Niloofar%20Abi.mp3"
TOKEN = '6414679474:AAHBrTFt5sCbbudkXHu3JvPrR_Pj50T30qs'

# تابع استارت که فایل را ارسال می‌کند
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # ارسال فایل به کاربر
    await update.message.reply_document(document=open(FILE_PATH, 'rb'))

async def main() -> None:
    # ساخت اپلیکیشن ربات با توکن
    app = ApplicationBuilder().token(TOKEN).build()

    # افزودن هندلر برای دستور استارت
    app.add_handler(CommandHandler("start", start))

    # شروع به دریافت به‌روزرسانی‌ها
    await app.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
