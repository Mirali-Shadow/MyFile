const TelegramBot = require('node-telegram-bot-api');
const fs = require('fs');
const path = require('path');

// توکن ربات خود را اینجا وارد کنید
const token = '6414679474:AAHBrTFt5sCbbudkXHu3JvPrR_Pj50T30qs';
const bot = new TelegramBot(token, { polling: true });

// ایجاد دکمه‌های شیشه‌ای
const downloadOptions = {
    reply_markup: {
        keyboard: [
            [{ text: 'دانلود موزیک 1' }],
            [{ text: 'دانلود موزیک 2' }],
            [{ text: 'دانلود موزیک 3' }],
            [{ text: 'دانلود موزیک 4' }],
            [{ text: 'دانلود موزیک 5' }],
            [{ text: 'دانلود موزیک 6' }],
            [{ text: 'دانلود موزیک 7' }],
            [{ text: 'دانلود موزیک 8' }],
            [{ text: 'دانلود موزیک 9' }],
            [{ text: 'دانلود موزیک 10' }],
            [{ text: 'اپلود موزیک' }],
        ],
        resize_keyboard: true,
        one_time_keyboard: true,
    }
};

// پیام خوش‌آمدگویی
bot.onText(/\/start/, (msg) => {
    const chatId = msg.chat.id;
    bot.sendMessage(chatId, "به ربات Shadow Rap خوش آمدید.\nبرای راهنمایی‌های بیشتر دستور /help را بفرستید.", downloadOptions);
});

// راهنمایی‌های بیشتر
bot.onText(/\/help/, (msg) => {
    const chatId = msg.chat.id;
    bot.sendMessage(chatId, "شما می‌توانید موزیک‌ها را دانلود کنید و همچنین موزیک‌های خود را آپلود کنید.");
});

// دریافت موزیک
bot.on('message', (msg) => {
    const chatId = msg.chat.id;

    // بررسی نوع پیام
    if (msg.text.startsWith('دانلود موزیک')) {
        const trackNumber = msg.text.split(' ')[2]; // شماره موزیک
        const filePath = path.join(__dirname, `benz${trackNumber}.mp3`); // فرض بر این است که موزیک‌ها به این صورت نام‌گذاری شده‌اند

        if (fs.existsSync(filePath)) {
            // ارسال موزیک
            bot.sendAudio(chatId, filePath, { caption: `شما موزیک ${trackNumber} را دانلود کردید.` });
        } else {
            bot.sendMessage(chatId, 'متاسفانه این موزیک وجود ندارد.');
        }
    }

    // بررسی دریافت فایل
    if (msg.document) {
        const fileExtension = path.extname(msg.document.file_name);

        // بررسی اینکه آیا فایل MP3 است
        if (fileExtension === '.mp3') {
            const filePath = path.join(__dirname, msg.document.file_name);

            // دانلود فایل
            bot.downloadFile(msg.document.file_id, __dirname).then(() => {
                bot.sendMessage(chatId, 'فایل با موفقیت دریافت شد!');
            }).catch((error) => {
                console.error(error);
                bot.sendMessage(chatId, 'خطا در دریافت فایل.');
            });
        } else {
            bot.sendMessage(chatId, 'لطفاً یک فایل معتبر (MP3) ارسال کنید.');
        }
    }
});
