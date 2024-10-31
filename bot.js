const TelegramBot = require('node-telegram-bot-api');

// توکن ربات خود را در اینجا قرار دهید
const token = '6414679474:AAHBrTFt5sCbbudkXHu3JvPrR_Pj50T30qs';
const bot = new TelegramBot(token, { polling: true });

// زمانی که کاربر ربات را شروع می‌کند
bot.onText(/\/start/, (msg) => {
    const chatId = msg.chat.id;
    const welcomeMessage = `به ربات Shadow Rap خوش اومدید.\nبرای راهنمایی های بیشتر دستور /help رو بفرستید.`;
    bot.sendMessage(chatId, welcomeMessage);
});

// زمانی که کاربر دستور /help را می‌فرستد
bot.onText(/\/help/, (msg) => {
    const chatId = msg.chat.id;
    const helpMessage = `این ربات به شما کمک می‌کند تا موزیک‌های مورد علاقه‌تان را به اشتراک بگذارید.\n\nدستورها:\n/start - شروع مکالمه با ربات\n/help - نمایش این راهنما`;
    bot.sendMessage(chatId, helpMessage);
});

// ارسال فایل xfile
bot.onText(/\/sendfile/, (msg) => {
    const chatId = msg.chat.id;
    const filePath = './xfile'; // مسیر فایل شما
    bot.sendDocument(chatId, filePath);
});
