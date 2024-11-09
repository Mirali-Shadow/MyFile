const TelegramBot = require('node-telegram-bot-api');
const token = '6414679474:AAHBrTFt5sCbbudkXHu3JvPrR_Pj50T30qs'; // توکن ربات شما
const bot = new TelegramBot(token, { polling: true });

// آیدی ادمین (شما) برای ارسال پیام‌ها به پیوی شما
const adminId = '7191775208'; // این را با آیدی تلگرام خود جایگزین کنید

// ذخیره پیام‌های کاربران برای ارسال پاسخ بعدی
let userMessages = {}; 

// دریافت پیام از کاربر
bot.on('message', (msg) => {
    const chatId = msg.chat.id;
    const text = msg.text;
    const username = msg.from.username || 'unknown_user';

    // ذخیره پیام کاربر برای ارسال پاسخ بعدی
    userMessages[chatId] = text;

    // ارسال پیام دریافتی به ادمین
    const messageToAdmin = `پیام جدید از کاربر @${username} (ID: ${chatId}):\n\n${text}`;
    bot.sendMessage(adminId, messageToAdmin);

    // ارسال تایید به کاربر
    bot.sendMessage(chatId, "پیام شما به ادمین ارسال شد. منتظر پاسخ باشید.");
});

// دریافت پیام از ادمین و ارسال به کاربر
bot.onText(/^\/reply (.+)$/, (msg, match) => {
    const chatId = msg.chat.id;
    const replyText = match[1]; // متن پاسخ ادمین
    const userId = msg.reply_to_message.chat.id;

    // بررسی اینکه آیا ادمین به پیام کاربری پاسخ می‌دهد یا نه
    if (userMessages[userId]) {
        bot.sendMessage(userId, `پاسخ ادمین: ${replyText}`);

        // ارسال تایید به ادمین که پاسخ به کاربر ارسال شد
        bot.sendMessage(chatId, "پاسخ به کاربر ارسال شد.");
        delete userMessages[userId]; // حذف پیام از حافظه پس از پاسخ
    } else {
        bot.sendMessage(chatId, "کاربر یافت نشد یا پیام موجود نیست.");
    }
});
