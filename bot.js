const TelegramBot = require('node-telegram-bot-api');

// Replace with your bot token
const token = '6414679474:AAHBrTFt5sCbbudkXHu3JvPrR_Pj50T30qs';
const bot = new TelegramBot(token, { polling: true });

// Welcome message when the bot is started
bot.onText(/\/start/, (msg) => {
    const chatId = msg.chat.id;
    const welcomeMessage = "به ربات Shadow Rap خوش اومدید\nبرای راهنمایی های بیشتر دستور /help رو بفرستید";
    bot.sendMessage(chatId, welcomeMessage);
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
    const musicOptions = "لطفا یکی از موزیک‌های زیر را انتخاب کنید:\n1. Gang Vaghei (BLH Remix)\n2. موزیک دوم\n3. موزیک سوم\nبرای ادامه، شماره موزیک را ارسال کنید یا برای برگشت 'برگشت' را بزنید.";

    bot.sendMessage(chatId, musicOptions);
});

// Handle music selection
bot.onText(/^(1|2|3)$/, (msg) => {
    const chatId = msg.chat.id;
    const selectedMusic = msg.text === '1' ? 'Gang Vaghei (BLH Remix)' : (msg.text === '2' ? 'موزیک دوم' : 'موزیک سوم');

    const channelCheckMessage = `${selectedMusic} را انتخاب کردید. برای دانلود، لطفاً دکمه تایید را بزنید.`;
    bot.sendMessage(chatId, channelCheckMessage, {
        reply_markup: {
            inline_keyboard: [[{ text: "تایید", callback_data: `confirm_${selectedMusic}` }]]
        }
    });
});

// Handle confirmation
bot.on('callback_query', (query) => {
    const chatId = query.message.chat.id;
    const callbackData = query.data;
    const selectedMusic = callbackData.split('_')[1];

    // Check if the user is a member of the channel
    const channelId = '@YourChannelID'; // replace with your channel ID

    bot.getChatMember(channelId, chatId).then((member) => {
        if (member.status === 'member' || member.status === 'administrator') {
            bot.sendMessage(chatId, "عضویت شما تایید شد. فایل موزیک ارسال می‌شود.");
            // Send the audio file
            const audioFilePath = './Gang Vaghei (BLH Remix).mp3'; // Path to your audio file
            bot.sendAudio(chatId, audioFilePath);
        } else {
            bot.sendMessage(chatId, "شما هنوز عضو نشده‌اید. لطفاً در کانال ما عضو شوید.");
        }
    }).catch(() => {
        bot.sendMessage(chatId, "شما هنوز عضو نشده‌اید. لطفاً در کانال ما عضو شوید.");
    });
});

// Handle the back command
bot.onText(/برگشت/, (msg) => {
    const chatId = msg.chat.id;
    const backMessage = "به منوی اصلی برگشتید. لطفاً یکی از گزینه‌ها را انتخاب کنید:\nدانلود موزیک\nاپلود موزیک";
    bot.sendMessage(chatId, backMessage);
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
