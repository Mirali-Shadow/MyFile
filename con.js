const TelegramBot = require('node-telegram-bot-api');

// توکن ربات خود را از BotFather وارد کنید
const token = 'YOUR_BOT_TOKEN';  // توکن ربات خود را از BotFather وارد کنید

// ساخت یک شیء ربات
const bot = new TelegramBot(token, { polling: true });

// لینک‌های خاص که خودتان تعریف می‌کنید
const fileLinks = {
  'getfile1': '/workspaces/MyFile/music/Pishro - Tamum Shode (featuring Kamyar).mp3',   // لینک getfile1 به فایل اول
  'getfile2': 'path_to_file_2',   // لینک getfile2 به فایل دوم
  'getfile3': 'path_to_file_3'    // لینک getfile3 به فایل سوم
};

// وقتی کاربر ربات را استارت می‌کند
bot.onText(/\/start/, (msg, match) => {
  const chatId = msg.chat.id;
  const text = match.input.split('=')[1];  // پارس کردن قسمت بعد از "=" در لینک

  if (text) {
    // چک کردن برای لینک خاص (مثل getfile1)
    if (fileLinks[text]) {
      const filePath = fileLinks[text];
      
      // ارسال فایل به کاربر
      bot.sendDocument(chatId, filePath).then(() => {
        console.log('File sent successfully!');
      }).catch(err => {
        console.error('Error sending file: ', err);
      });
    } else {
      // اگر لینک نامعتبر باشد
      bot.sendMessage(chatId, 'سلام! لینک نامعتبر است یا فایل پیدا نشد.');
    }
  } else {
    // در صورتی که هیچ لینک خاصی دریافت نشود
    bot.sendMessage(chatId, 'سلام! برای دریافت فایل، لطفاً از لینک خاص استفاده کنید.');
  }
});

// وقتی کاربر با لینک خاص به ربات می‌آید
bot.on('message', (msg) => {
  const chatId = msg.chat.id;
  const text = msg.text;
  
  // بررسی اینکه آیا متن ارسالی یکی از لینک‌های خاص است
  if (text && text.startsWith('https://t.me/your_bot_name?start=')) {
    const command = text.split('=')[1];  // استخراج دستور از لینک
    if (fileLinks[command]) {
      // ارسال فایل مطابق با لینک
      const filePath = fileLinks[command];
      bot.sendDocument(chatId, filePath).then(() => {
        console.log('File sent successfully!');
      }).catch(err => {
        console.error('Error sending file: ', err);
      });
    } else {
      bot.sendMessage(chatId, 'لینک نامعتبر است یا فایل پیدا نشد.');
    }
  }
});
