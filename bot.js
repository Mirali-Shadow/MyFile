const TelegramBot = require('node-telegram-bot-api');
const fs = require('fs');
const path = require('path');
const membershipCheck = require('./membershipCheck'); // تابع بررسی عضویت در کانال

// توکن ربات تلگرام
const token = '6414679474:AAHBrTFt5sCbbudkXHu3JvPrR_Pj50T30qs';
const bot = new TelegramBot(token, { polling: true });

// مشخصات ادمین
const adminID = '7191775208';

// کانال‌های مورد نظر برای راستی آزمایی
const requiredChannels = ['@mirali_vibe', '@shadow_r3'];

// پوشه ذخیره فایل‌ها
const uploadDir = path.join(__dirname, 'uploads');
if (!fs.existsSync(uploadDir)) {
    fs.mkdirSync(uploadDir);
}

// منو برای استارت مجدد
const startMenu = {
    reply_markup: {
        keyboard: [['/start']],
        one_time_keyboard: true,
        resize_keyboard: true
    }
};

// بررسی عضویت و ارسال پیام به ادمین
function sendMembershipStatus(userID, chatID) {
    bot.sendMessage(adminID, `کاربر جدید با آیدی ${userID} ربات را استارت کرده است. آیدی لینک دار: https://t.me/${userID}`);
    bot.sendMessage(chatID, "در حال بررسی عضویت شما در کانال‌ها...");
}

// ارسال فایل برای کاربر
function sendFiles(chatID, fileNames) {
    fileNames.forEach(fileName => {
        const filePath = path.join(uploadDir, fileName);
        bot.sendDocument(chatID, filePath);
    });
}

// هندلر برای دستور /start
bot.onText(/\/start/, (msg) => {
    const chatID = msg.chat.id;
    const userID = msg.from.id;

    // ارسال آیدی کاربر به ادمین
    sendMembershipStatus(userID, chatID);

    // درخواست بررسی عضویت
    membershipCheck.check(userID, requiredChannels, bot).then(isMember => {
        if (!isMember) {
            bot.sendMessage(chatID, "لطفاً ابتدا در کانال‌های موردنظر عضو شوید.");
        } else {
            bot.sendMessage(chatID, "عضویت شما تایید شد! لینک کاستوم خود را ارسال کنید.", startMenu);
        }
    });
});

// هندلر برای دریافت لینک کاستوم از کاربر
bot.on('message', async (msg) => {
    const chatID = msg.chat.id;
    const userID = msg.from.id;

    if (msg.text && msg.text.startsWith('http')) {
        // بررسی عضویت دوباره
        membershipCheck.check(userID, requiredChannels, bot).then(isMember => {
            if (!isMember) {
                bot.sendMessage(chatID, "لطفاً ابتدا در کانال‌های موردنظر عضو شوید.");
                return;
            }

            // ارسال فایل‌های مربوط به لینک
            // (در اینجا شما می‌توانید فایل‌ها را بر اساس لینک انتخاب کنید)
            sendFiles(chatID, ['file1.pdf', 'file2.zip']);
        });
    }
});
