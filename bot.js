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
    //bot.sendMessage(chatId, 'سلام! خوش آمدید به ربات ما!');
});

// مدیریت پیام‌ها
bot.on('message', (msg) => {
    const chatId = msg.chat.id;

    // چک کردن آیا پیام شامل لینک اختصاصی است
    if (msg.text === 'https://t.me/shadow_byte_bot?start=getfil') {
        // اگر لینک درست بود، فایل ارسال شود
        bot.sendDocument(chatId, fileUrl)
            .then(() => {
                console.log(`فایل به ${chatId} ارسال شد`);
                // هیچ پیامی در اینجا ارسال نمی‌شود
            })
            .catch((error) => {
                console.error(`خطا در ارسال فایل: ${error}`);
                // می‌توانید در صورت نیاز پیامی ارسال کنید
            });
    }
});

// شروع ربات
console.log('ربات در حال اجراست...');
