const TelegramBot = require('node-telegram-bot-api');
const fs = require('fs');

// Replace with your bot token
const token = '6414679474:AAHBrTFt5sCbbudkXHu3JvPrR_Pj50T30qs';
const bot = new TelegramBot(token, { polling: true });

// Welcome message when the bot is started
bot.onText(/\/start/, (msg) => {
    const chatId = msg.chat.id;
    const welcomeMessage = "به ربات Shadow Rap خوش اومدید\nبرای راهنمایی های بیشتر دستور /help رو بفرستید";
    bot.sendMessage(chatId, welcomeMessage, {
        reply_markup: {
            keyboard: [
                [{ text: "دانلود موزیک" }],
                [{ text: "اپلود موزیک" }]
            ],
            resize_keyboard: true,
            one_time_keyboard: true
        }
    });
});

// Help command
bot.onText(/\/help/, (msg) => {
    const chatId = msg.chat.id;
    const helpMessage = "برای دانلود موزیک، دکمه 'دانلود موزیک' را فشار دهید.\nبرای ارسال موزیک، دکمه 'اپلود موزیک' را فشار دهید.";
    bot.sendMessage(chatId, helpMessage);
});

// Download music menu
bot.onText(/دانلود موزیک/, (msg) => {
    const chatId = msg.chat.id;
    bot.sendMessage(chatId, "برای دانلود موزیک 'Gang Vaghei (BLH Remix)' شما باید در کانال‌های زیر عضو شوید:", {
        reply_markup: {
            inline_keyboard: [
                [
                    { text: "کانال 1", url: "https://t.me/MiRALi_ViBE" },
                    //{ text: "کانال2", url: "https://t.me/mirali_vibe" }
                ],
                [{ text: "برگشت", callback_data: "back_to_main" }]
            ]
        }
    });
});

// Upload music menu
bot.onText(/اپلود موزیک/, (msg) => {
    const chatId = msg.chat.id;
    const uploadMessage = "لطفا موزیک مورد نظر را ارسال کنید.";
    bot.sendMessage(chatId, uploadMessage);
});

// Handle incoming audio files
bot.on('audio', (msg) => {
    const chatId = msg.chat.id;
    const fileId = msg.audio.file_id;

    // Download the file and send a confirmation
    bot.downloadFile(fileId, './').then((filePath) => {
        bot.sendMessage(chatId, "فایل با موفقیت دریافت شد.");
    }).catch(() => {
        bot.sendMessage(chatId, "لطفا یک فایل معتبر ارسال کنید.");
    });
});

// Handle callback queries (for the back button)
bot.on('callback_query', (query) => {
    const chatId = query.message.chat.id;
    const callbackData = query.data;

    if (callbackData === 'back_to_main') {
        bot.sendMessage(chatId, "به منوی اصلی برگشتید.", {
            reply_markup: {
                keyboard: [
                    [{ text: "دانلود موزیک" }],
                    [{ text: "اپلود موزیک" }]
                ],
                resize_keyboard: true,
                one_time_keyboard: true
            }
        });
    }
});
