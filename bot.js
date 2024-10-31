const TelegramBot = require('node-telegram-bot-api');
const path = require('path'); // برای تعیین مسیر فایل

// توکن ربات خود را در اینجا قرار دهید
const token = '6414679474:AAHBrTFt5sCbbudkXHu3JvPrR_Pj50T30qs';
const bot = new TelegramBot(token, { polling: true });

// زمانی که کاربر ربات را شروع می‌کند
bot.onText(/\/start/, (msg) => {
    const chatId = msg.chat.id;

    const options = {
        reply_markup: {
            inline_keyboard: [
                [
                    { text: '🎶 موزیک‌ها', callback_data: 'music' },
                    { text: '📅 تقویم', callback_data: 'calendar' }
                ],
                [
                    { text: '🎵 ارسال موزیک benz.mp3', callback_data: 'send_music' },
                    { text: '📖 راهنما', callback_data: 'help' }
                ]
            ]
        }
    };

    bot.sendMessage(chatId, 'به ربات Shadow Rap خوش اومدید. لطفا یکی از گزینه‌ها را انتخاب کنید:', options);
});

// مدیریت Callback برای دکمه‌های Inline
bot.on('callback_query', (query) => {
    const chatId = query.message.chat.id;

    if (query.data === 'music') {
        bot.sendMessage(chatId, 'شما موزیک‌ها را انتخاب کردید.');
    } else if (query.data === 'calendar') {
        bot.sendMessage(chatId, 'شما تقویم را انتخاب کردید.');
    } else if (query.data === 'help') {
        bot.sendMessage(chatId, 'این ربات به شما کمک می‌کند تا موزیک‌های مورد علاقه‌تان را به اشتراک بگذارید.');
    } else if (query.data === 'send_music') {
        // مسیر فایل موزیک benz.mp3
        const musicPath = path.join(__dirname, 'benz.mp3'); // فرض کنید فایل benz.mp3 در همان پوشه bot.js قرار دارد

        bot.sendAudio(chatId, musicPath)
            .then(() => {
                bot.answerCallbackQuery(query.id, { text: 'موزیک benz.mp3 ارسال شد.' });
            })
            .catch((error) => {
                console.error('Error sending audio:', error);
                bot.answerCallbackQuery(query.id, { text: 'خطا در ارسال موزیک. لطفا دوباره تلاش کنید.' });
            });
    }
});
