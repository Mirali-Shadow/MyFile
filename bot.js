// بارگذاری ماژول‌های لازم
const TelegramBot = require('node-telegram-bot-api');
const path = require('path');
const fs = require('fs');

// توکن ربات خود را در اینجا وارد کنید
const token = '6414679474:AAHBrTFt5sCbbudkXHu3JvPrR_Pj50T30qs';

// ایجاد یک ربات با حالت polling
const bot = new TelegramBot(token, { polling: true });

// در صورتی که کاربر ربات را استارت کند
bot.onText(/\/start/, (msg) => {
    const chatId = msg.chat.id;

    // مسیر فایل xfile را تنظیم کنید
    const filePath = path.join(__dirname, 'xfile'); // فرض می‌کنیم xfile در همان پوشه است

    // بررسی اینکه آیا فایل وجود دارد
    if (fs.existsSync(filePath)) {
        // ارسال فایل به کاربر
        bot.sendDocument(chatId, filePath)
            .then(() => {
                bot.sendMessage(chatId, 'فایل xfile ارسال شد!');
            })
            .catch((error) => {
                console.error('خطا در ارسال فایل:', error);
                bot.sendMessage(chatId, 'متاسفانه خطایی در ارسال فایل رخ داد.');
            });
    } else {
        bot.sendMessage(chatId, 'فایل xfile پیدا نشد.');
    }
});
