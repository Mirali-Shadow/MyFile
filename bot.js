// کتابخانه مورد نیاز را وارد کنید
const TelegramBot = require('node-telegram-bot-api');
const fs = require('fs');

// توکن ربات خود را جایگزین کنید
const token = '6414679474:AAHBrTFt5sCbbudkXHu3JvPrR_Pj50T30qs';

// یک نمونه از ربات ایجاد کنید
const bot = new TelegramBot(token, { polling: true });

// نام فایلی که می‌خواهید ارسال کنید را مشخص کنید
const fileName = 'Seft (Djsajjad1 & BLH Remix).mp3'; // نام فایل را به دلخواه تغییر دهید

// لینک خاصی که کاربران روی آن کلیک می‌کنند
const specialLink = 'https://t.me/Shadow_byte_Bot?start=n2s1ds2d2s7d545s'; // لینک واقعی خود را جایگزین کنید

// گوش دادن به پیام‌ها
bot.onText(/\/start/, (msg) => {
    const chatId = msg.chat.id;
    bot.sendMessage(chatId, `خوش آمدید! برای دریافت فایل خود اینجا کلیک کنید: ${specialLink}`);
});

// تابعی برای ارسال فایل
function sendFile(chatId) {
    // ارسال فایل به کاربر
    bot.sendDocument(chatId, fileName)
        .then(() => {
            console.log(`فایل به ${chatId} ارسال شد`);

            // بعد از 1 دقیقه (60000 میلی‌ثانیه) فایل را حذف کنید
            setTimeout(() => {
                // بررسی کنید که آیا فایل وجود دارد و آن را حذف کنید
                if (fs.existsSync(fileName)) {
                    fs.unlinkSync(fileName); // حذف فایل
                    console.log(`فایل ${fileName} حذف شد.`);
                }
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
