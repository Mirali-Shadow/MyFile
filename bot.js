const TelegramBot = require('node-telegram-bot-api');
const path = require('path');

// توکن ربات خود را در اینجا قرار دهید
const token = '6414679474:AAHBrTFt5sCbbudkXHu3JvPrR_Pj50T30qs';
const bot = new TelegramBot(token, { polling: true });

// زمانی که کاربر ربات را شروع می‌کند
bot.onText(/\/start/, (msg) => {
    const chatId = msg.chat.id;

    // گزینه‌های منوی اصلی
    const options = {
        reply_markup: {
            inline_keyboard: [
                [
                    { text: '📥 دانلود موزیک', callback_data: 'download_music' },
                    { text: '📤 آپلود موزیک', callback_data: 'upload_music' }
                ]
            ]
        }
    };

    // ارسال پیام خوشامدگویی
    bot.sendMessage(chatId, 'به ربات Shadow Rap خوش اومدید. لطفا یکی از گزینه‌ها را انتخاب کنید:', options);
});

// مدیریت Callback برای دکمه‌های Inline
bot.on('callback_query', (query) => {
    const chatId = query.message.chat.id;

    // بررسی انتخاب دانلود موزیک
    if (query.data === 'download_music') {
        sendMusicList(chatId);
    } 
    // بررسی انتخاب آپلود موزیک
    else if (query.data === 'upload_music') {
        bot.sendMessage(chatId, 'لطفاً فایل موزیک یا فایلی که می‌خواهید ارسال کنید را بفرستید.');
        bot.once('message', (msg) => {
            if (msg.document) {
                handleFileUpload(chatId, msg.document);
            } else {
                bot.sendMessage(chatId, 'لطفاً یک فایل معتبر ارسال کنید.');
            }
        });
    } 
    // ارسال موزیک انتخاب شده
    else if (query.data.startsWith('music')) {
        const musicPath = path.join(__dirname, query.data); // مسیر فایل موزیک
        bot.sendAudio(chatId, musicPath)
            .then(() => {
                bot.answerCallbackQuery(query.id, { text: 'موزیک ارسال شد.' });
            })
            .catch((error) => {
                console.error('Error sending audio:', error);
                bot.answerCallbackQuery(query.id, { text: 'خطا در ارسال موزیک. لطفا دوباره تلاش کنید.' });
            });
    }
});

// تابع برای ارسال لیست موزیک‌ها
function sendMusicList(chatId) {
    const musicOptions = {
        reply_markup: {
            inline_keyboard: []
        }
    };

    // لیست 100 موزیک
    for (let i = 1; i <= 100; i++) {
        const musicFileName = `music${i}.mp3`; // فرض کنید نام موزیک‌ها به صورت music1.mp3, music2.mp3,... باشد
        const buttonText = `🎵 موزیک ${i}`; // متن دکمه
        musicOptions.reply_markup.inline_keyboard.push([{ text: buttonText, callback_data: musicFileName }]);
    }

    bot.sendMessage(chatId, 'لطفا موزیک مورد نظر خود را انتخاب کنید:', musicOptions);
}

// تابع مدیریت آپلود فایل
function handleFileUpload(chatId, document) {
    const fileId = document.file_id;

    // ارسال پیام به کاربر مبنی بر دریافت فایل
    bot.sendMessage(chatId, 'فایل شما دریافت شد. پس از بررسی، منتشر خواهد شد.');

    // دریافت لینک فایل
    bot.getFile(fileId).then((file) => {
        const filePath = `https://api.telegram.org/file/bot${token}/${file.file_path}`;
        console.log('File to be reviewed:', filePath);
        // در اینجا می‌توانید یک سیستم مدیریت برای بررسی و انتشار فایل‌ها پیاده‌سازی کنید
    }).catch((error) => {
        console.error('Error getting file:', error);
    });
}
