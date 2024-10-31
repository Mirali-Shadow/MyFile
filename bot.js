const TelegramBot = require('node-telegram-bot-api');

// توکن ربات تلگرام خود را اینجا وارد کنید
const token = '6414679474:AAHBrTFt5sCbbudkXHu3JvPrR_Pj50T30qs';

// ساخت ربات
const bot = new TelegramBot(token, { polling: true });

// پیغام خوش‌آمدگویی
bot.onText(/\/start/, (msg) => {
    const chatId = msg.chat.id;
    bot.sendMessage(chatId, 'به ربات Shadow Rap خوش اومدید. برای راهنمایی های بیشتر دستور /help رو بفرستید.');

    // منوی شیشه‌ای دانلود موزیک و اپلود موزیک
    const options = {
        reply_markup: {
            inline_keyboard: [
                [
                    { text: 'دانلود موزیک', callback_data: 'download_music' },
                    { text: 'آپلود موزیک', callback_data: 'upload_music' }
                ]
            ]
        }
    };
    bot.sendMessage(chatId, 'لطفا یکی از گزینه‌ها را انتخاب کنید:', options);
});

// راهنمای ربات
bot.onText(/\/help/, (msg) => {
    const chatId = msg.chat.id;
    const helpMessage = `
        راهنمای ربات:
        - برای دانلود موزیک، گزینه "دانلود موزیک" را انتخاب کنید.
        - برای ارسال موزیک به ربات، گزینه "آپلود موزیک" را انتخاب کنید.
    `;
    bot.sendMessage(chatId, helpMessage);
});

// منوی دانلود موزیک
bot.on('callback_query', (query) => {
    const chatId = query.message.chat.id;

    if (query.data === 'download_music') {
        const downloadOptions = {
            reply_markup: {
                inline_keyboard: [
                    [
                        { text: 'موزیک 1', callback_data: 'send_music_1' },
                        { text: 'موزیک 2', callback_data: 'send_music_2' },
                    ],
                    // می‌توانید شیشه‌های بیشتر اضافه کنید
                ]
            }
        };
        bot.sendMessage(chatId, 'لطفا موزیک مورد نظر خود را انتخاب کنید:', downloadOptions);
    }

    // ارسال موزیک
    if (query.data === 'send_music_1') {
        bot.sendAudio(chatId, 'Gang Vaghei (BLH Remix).mp3');
    }
    if (query.data === 'send_music_2') {
        // جایگزین کنید با نام فایل موزیک
        bot.sendAudio(chatId, 'YOUR_OTHER_MUSIC_FILE.mp3');
    }
});

// منوی آپلود موزیک
bot.on('callback_query', (query) => {
    const chatId = query.message.chat.id;

    if (query.data === 'upload_music') {
        bot.sendMessage(chatId, 'لطفا فایل موزیک خود را ارسال کنید.');
    }
});

// دریافت فایل آپلود شده
bot.on('document', (msg) => {
    const chatId = msg.chat.id;
    const fileType = msg.document.mime_type;

    // بررسی نوع فایل
    if (fileType === 'audio/mpeg') {
        bot.sendMessage(chatId, 'فایل شما دریافت شد. پس از بررسی منتشر خواهد شد.');
        // اینجا می‌توانید کد بررسی و ذخیره فایل را اضافه کنید
    } else {
        bot.sendMessage(chatId, 'لطفا یک فایل معتبر ارسال کنید.');
    }
});
