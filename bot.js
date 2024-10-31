// کتابخانه مورد نیاز را وارد کنید
const TelegramBot = require('node-telegram-bot-api');

// توکن ربات شما
const token = '6414679474:AAHBrTFt5sCbbudkXHu3JvPrR_Pj50T30qs'; // توکن ربات شما

// یک نمونه از ربات ایجاد کنید
const bot = new TelegramBot(token, { polling: true });

// لینک مستقیم به فایل شما در GitHub
const fileUrl = 'https://raw.githubusercontent.com/Mirali-Shadow/MyFile/2fa16293c554cc38e87fa56831e94d52f0ef3a5d/Seft%20(Djsajjad1%20%26%20BLH%20Remix).mp3';

// گوش دادن به پیام‌ها
bot.onText(/\/start/, (msg) => {
    const chatId = msg.chat.id;
    // ارسال پیام سلام به کاربر
    bot.sendMessage(chatId, 'سلام! خوش آمدید به ربات ما!');
});

// مدیریت دستور start با پارامتر
bot.on('message', (msg) => {
    const chatId = msg.chat.id;
    if (msg.text && msg.text.startsWith('/start')) {
        const params = msg.text.split(' '); // جدا کردن پارامترها
        if (params[1] === 'getfile') {
            sendFile(chatId); // ارسال فایل اگر پارامتر getfile باشد
        }
    } else if (msg.text === 'https://t.me/shadow_byte_bot?start=getfile') {
        // ارسال فایل بلافاصله با کلیک بر روی لینک اختصاصی
        sendFile(chatId); // ارسال فایل بلافاصله
    }
});

// تابعی برای ارسال فایل
function sendFile(chatId) {
    // ارسال فایل به کاربر از لینک مستقیم
    bot.sendDocument(chatId, fileUrl)
        .then(() => {
            console.log(`فایل به ${chatId} ارسال شد`);
        })
        .catch((error) => {
            console.error(`خطا در ارسال فایل: ${error}`);
        });
}

// شروع ربات
console.log('ربات در حال اجراست...');
