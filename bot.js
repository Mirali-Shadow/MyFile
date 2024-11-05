const TelegramBot = require('node-telegram-bot-api');
const fs = require('fs');
const path = require('path');

// توکن ربات خود را در اینجا وارد کنید
const token = 'YOUR_TELEGRAM_BOT_TOKEN';
const bot = new TelegramBot(token, { polling: true });

// لیست آهنگ‌ها؛ فرض کنید فایل‌های صوتی در پوشه‌ای به نام 'music' ذخیره شده‌اند
const musicDir = path.join(__dirname, 'music');
const musicFiles = fs.readdirSync(musicDir).filter(file => file.endsWith('.mp3'));

// سایز آلبوم
const albumSize = 3;

// تقسیم آهنگ‌ها به آلبوم‌های کوچک‌تر
const splitToAlbums = (files, size) => {
    const albums = [];
    for (let i = 0; i < files.length; i += size) {
        albums.push(files.slice(i, i + size));
    }
    return albums;
};

// فرمان /start را به ربات اضافه می‌کنیم
bot.onText(/\/start/, (msg) => {
    const chatId = msg.chat.id;

    // پیام خوش‌آمدگویی با دکمه‌های شیشه‌ای
    bot.sendMessage(chatId, 'Welcome! Choose an option below:', {
        reply_markup: {
            inline_keyboard: [
                [{ text: '🎶 Send me an album', callback_data: 'send_album' }]
            ]
        }
    });
});

// هندلر برای دکمه‌های شیشه‌ای
bot.on('callback_query', (query) => {
    const chatId = query.message.chat.id;

    if (query.data === 'send_album') {
        const albums = splitToAlbums(musicFiles, albumSize);

        albums.forEach((album, index) => {
            const mediaGroup = album.map(file => ({
                type: 'audio',
                media: { source: path.join(musicDir, file) },
                caption: `Track ${index + 1}`
            }));

            // ارسال هر آلبوم به صورت گروهی
            bot.sendMediaGroup(chatId, mediaGroup)
                .then(() => {
                    bot.sendMessage(chatId, `Album ${index + 1} sent!`);
                })
                .catch(err => {
                    console.error('Error sending album:', err);
                });
        });

        // پاسخ به کاربر که درخواستش دریافت شد
        bot.answerCallbackQuery(query.id, { text: 'Sending your album!' });
    }
});
