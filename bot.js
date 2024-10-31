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

// مدیریت پیام‌ها
bot.on('message', (msg) => {
    const chatId = msg.chat.id;

    // چک کردن آیا پیام شامل لینک اختصاصی است
    if (msg.text) {
        // بررسی لینک اختصاصی
        if (msg.text === 'https://t.me/shadow_byte_bot?start=getfile') {
            sendFile(chatId);
        } else {
            // اگر پیام دیگر باشد، می‌توانیم به کاربر بگوییم که لینک را ارسال کند
            bot.sendMessage(chatId, 'لطفا لینک اختصاصی را برای دریافت فایل ارسال کنید.');
        }
    }
});

// تابعی برای ارسال فایل
function sendFile(chatId) {
    // ارسال فایل به کاربر از لینک مستقیم
    bot.sendDocument(chatId, fileUrl)
        .then(() => {
            console.log(`فایل به ${chatId} ارسال شد`);
            // پس از ارسال فایل، می‌توانیم یک پیام تأیید ارسال کنیم
            bot.sendMessage(chatId, 'فایل شما با موفقیت ارسال شد!');
        })
        .catch((error) => {
            console.error(`خطا در ارسال فایل: ${error}`);
            // در صورت بروز خطا، پیام خطا به کاربر ارسال کنید
            bot.sendMessage(chatId, 'متاسفانه در ارسال فایل خطایی پیش آمد. لطفا دوباره امتحان کنید.');
        });
}

// شروع ربات
console.log('ربات در حال اجراست...');
