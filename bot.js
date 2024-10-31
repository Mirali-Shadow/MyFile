const TelegramBot = require('node-telegram-bot-api');
const path = require('path');

// توکن ربات شما
const token = '6414679474:AAHBrTFt5sCbbudkXHu3JvPrR_Pj50T30qs';
const bot = new TelegramBot(token, { polling: true });

// شناسه کانال مورد نظر (باید با '@' شروع شود)
const channelId = 'mirali_vibe'; // به جای YOUR_CHANNEL_ID، نام کانال خود را قرار دهید

// کد برای دریافت لینک اختصاصی و ارسال پیام
bot.onText(/\/start/, (msg) => {
  const chatId = msg.chat.id;
  bot.sendMessage(chatId, 'برای دریافت فایل باید عضو کانال شوید. آیا می‌خواهید به کانال بپیوندید؟', {
    reply_markup: {
      inline_keyboard: [
        [
          {
            text: 'عضو کانال شوید',
            url: `https://t.me/${channelId}`,
          },
        ],
        [
          {
            text: 'بررسی عضویت',
            callback_data: 'check_membership',
          },
        ],
      ],
    },
  });
});

// بررسی
