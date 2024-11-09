const TelegramBot = require('node-telegram-bot-api');

// توکن ربات تلگرام خود را از BotFather وارد کنید
const token = '6352712951:AAHtDi_d8NfcmpaYYE9uqX9jZGD-6lsyj40';  // توکن ربات خود را از BotFather وارد کنید

// ساخت یک شیء ربات
const bot = new TelegramBot(token, { polling: true });

// لینک‌های خاص که خودتان تعریف می‌کنید
const fileLinks = {
  'getfil1': 'https://github.com/Mirali-Shadow/MyFile/raw/refs/heads/main/music/Pishro%20-%20Tamum%20Shode%20(featuring%20Kamyar).mp3',   // لینک مستقیم به فایل اول
  'getfil2': 'https://raw.githubusercontent.com/username/repository/branch/files/myfile2.pdf',   // لینک مستقیم به فایل دوم
  'getfil3': 'https://raw.githubusercontent.com/username/repository/branch/files/myfile3.pdf'    // لینک مستقیم به فایل سوم
};

// وقتی که کاربر ربات را استارت می‌کند
bot.onText(/\/start/, (msg, match) => {
  const chatId = msg.chat.id;

  // بررسی اینکه آیا کاربر روی لینک خاص کلیک کرده است
  const text = match.input.split('=')[1]; // پارس کردن قسمت بعد از "=" در لینک

  if (text && fileLinks[text]) {
    // اگر دستور معتبر باشد، فایل ارسال می‌شود
    const fileUrl = fileLinks[text];
    
    // ارسال فایل از URL گیت‌هاب
    bot.sendDocument(chatId, fileUrl)
      .then(() => {
        console.log('File sent from URL!');
      })
      .catch(err => {
        console.error('Error sending file from URL: ', err);
      });
  } else {
    // اگر لینک نامعتبر باشد
    bot.sendMessage(chatId, 'لینک نامعتبر است یا فایل پیدا نشد. لطفاً از لینک‌های معتبر استفاده کنید.');
  }
});
