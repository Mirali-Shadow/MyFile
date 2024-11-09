const TelegramBot = require('node-telegram-bot-api');

// توکن ربات تلگرام خود را از BotFather وارد کنید
const token = '6414679474:AAHBrTFt5sCbbudkXHu3JvPrR_Pj50T30qs';  // توکن ربات خود را از BotFather وارد کنید

// ساخت یک شیء ربات
const bot = new TelegramBot(token, { polling: true });

// فایل‌هایی که باید ارسال شوند
const fileLinks = {
  'getfile1': 'https://github.com/Mirali-Shadow/MyFile/raw/refs/heads/main/music/Pishro%20-%20Tamum%20Shode%20(featuring%20Kamyar).mp3',   // مسیر یا URL فایل اول
  'getfile2': 'music/Seft (Djsajjad1 & BLH Remix).mp3',   // مسیر یا URL فایل دوم
  'getfile3': '/workspaces/MyFile/music/benz.mp3'    // مسیر یا URL فایل سوم
};

// وقتی که کاربر ربات را استارت می‌کند
bot.onText(/\/start/, (msg, match) => {
  const chatId = msg.chat.id;

  // بررسی اینکه آیا کاربر روی لینک خاص کلیک کرده است
  const text = match.input.split('=')[1]; // پارس کردن قسمت بعد از "=" در لینک

  if (text && fileLinks[text]) {
    // اگر دستور معتبر باشد، فایل ارسال می‌شود
    const filePath = fileLinks[text];
    bot.sendDocument(chatId, filePath)
      .then(() => {
        console.log('File sent successfully!');
      })
      .catch(err => {
        console.error('Error sending file: ', err);
      });
  } else {
    // در صورتی که لینک نامعتبر باشد
    bot.sendMessage(chatId, 'لینک نامعتبر است یا فایل پیدا نشد. لطفاً از لینک‌های معتبر استفاده کنید.');
  }
});

// این کد برای هنگامی است که کاربر به ربات پیام بفرستد
bot.on('message', (msg) => {
  const chatId = msg.chat.id;
  const text = msg.text;

  // چک کردن اینکه آیا متن پیام شامل لینک خاص است یا خیر
  if (text && text.startsWith('https://t.me/shadow_byte_bot?start=')) {
    const command = text.split('=')[1];  // استخراج دستور از لینک
    if (fileLinks[command]) {
      // ارسال فایل مطابق با دستور
      const filePath = fileLinks[command];
      bot.sendDocument(chatId, filePath)
        .then(() => {
          console.log('File sent successfully!');
        })
        .catch(err => {
          console.error('Error sending file: ', err);
        });
    } else {
      bot.sendMessage(chatId, 'لینک نامعتبر است یا فایل پیدا نشد.');
    }
  }
});
