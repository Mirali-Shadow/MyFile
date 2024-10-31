const TelegramBot = require('node-telegram-bot-api');
const path = require('path');

// توکن ربات شما
const token = '6414679474:AAHBrTFt5sCbbudkXHu3JvPrR_Pj50T30qs';
const bot = new TelegramBot(token, { polling: true });

// شناسه کانال مورد نظر (باید با '@' شروع شود)
const channelId = 'mirali_vibe';

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

// بررسی عضویت کاربر در کانال
bot.on('callback_query', async (query) => {
  const chatId = query.from.id;

  if (query.data === 'check_membership') {
    try {
      const memberStatus = await bot.getChatMember(channelId, chatId);

      if (memberStatus.status === 'member' || memberStatus.status === 'administrator' || memberStatus.status === 'creator') {
        // اگر کاربر عضو کانال بود، فایل را ارسال کنید
        const filePath = path.join(__dirname, 'Gang Vaghei (BLH Remix).mp3'); // مسیر فایل
        bot.sendAudio(chatId, filePath);
      } else {
        // اگر کاربر عضو کانال نبود
        bot.sendMessage(chatId, 'شما هنوز عضو کانال نشده‌اید.');
      }
    } catch (error) {
      console.error(error);
      bot.sendMessage(chatId, 'خطا در بررسی عضویت. لطفاً دوباره امتحان کنید.');
    }
  }
});
