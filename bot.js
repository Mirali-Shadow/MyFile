const TelegramBot = require('node-telegram-bot-api');

// توکن ربات شما
const token = '6414679474:AAHBrTFt5sCbbudkXHu3JvPrR_Pj50T30qs';
const bot = new TelegramBot(token, { polling: true });

// پاسخ به پیام "/start"
bot.onText(/\/start/, (msg) => {
  const chatId = msg.chat.id;
  bot.sendMessage(chatId, 'به ربات تلگرام خوش آمدید!');
});

// پاسخ به پیام‌ها
bot.on('message', (msg) => {
  const chatId = msg.chat.id;
  bot.sendMessage(chatId, `شما گفتید: ${msg.text}`);
});
