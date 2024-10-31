// کتابخانه مورد نیاز را وارد کنید
const TelegramBot = require('node-telegram-bot-api');
const fs = require('fs');

// توکن ربات خود را جایگزین کنید
const token = '6414679474:AAHBrTFt5sCbbudkXHu3JvPrR_Pj50T30qs'; // توکن ربات خود را وارد کنید

// یک نمونه از ربات ایجاد کنید
const bot = new TelegramBot(token, { polling: true });

// لینک مستقیم به فایل شما در GitHub
const fileUrl = 'https://raw.githubusercontent.com/Mirali-Shadow/MyFile/2fa16293c554cc38e87fa56831e94d52f0ef3a5d/Seft%20(Djsajjad1%20%26%20BLH%20Remix).mp3';

// لینک خاصی که کاربران روی آن کلیک می‌کنند
const specialLink = 'https://t.me/Shadow_byte_bot?start=kh3sdg1fd51gx'; // نام کاربری ربات خود را وارد کنید

// گوش دادن به پیام‌ها
bot.onText(/\/start/, (msg) => {
    const chatId = msg.chat.id;
    bot.sendMessage(chatId, `خوش آمدید! برای دریافت فایل خود اینجا کلیک کنید: ${specialLink}`);
});

// تابعی برای ارسال فایل
function sendFile(chatId) {
    // ارسال فایل به کاربر از لینک مستقیم
    bot.sendDocument(chatId, fileUrl)
        .then(() => {
            console.log(`فایل به ${chatId} ارسال شد`);

            // حذف فایل بعد از 1 دقیقه (60000 میلی‌ثانیه)
            setTimeout(() => {
                console.log(`فایل ${fileUrl} پس از 1 دقیقه قابل حذف است، اما فایل در GitHub حذف نمی‌شود.`);
            }, 60000); // 1 دقیقه
        })
        .catch((error) => {
            console.error(`خطا در ارسال فایل: ${error}`);
        });
}

// مدیریت کلیک روی لینک خاص
bot.onText(/\/getfile/, (msg) => {
    const chatId = msg.chat.id;
    sendFile(chatId); // فراخوانی تابع برای ارسال فایل
});

// شروع ربات
console.log('ربات در حال اجراست...');
