const TelegramBot = require('node-telegram-bot-api');
const { checkMembership } = require('./membershipCheck');
const { sendUserId } = require('./idSend');

const token = '6414679474:AAHBrTFt5sCbbudkXHu3JvPrR_Pj50T30qs';
const bot = new TelegramBot(token, { polling: true });

const requiredChannels = ["@MIRALI_VIBE", "@shadow_R3"];

bot.onText(/\/start/, (msg) => {
    const chatId = msg.chat.id;
    const userId = msg.from.id;
    const username = msg.from.username;

    // ارسال آیدی عددی و نام کاربری به ادمین
    sendUserId(userId, username, bot);

    // پیام خوش‌آمدگویی
    bot.sendMessage(chatId, "خوش آمدید! برای آپلود فایل ابتدا عضو کانال‌های ما شوید و سپس دستور /upload را وارد کنید.");
});

bot.onText(/\/upload/, async (msg) => {
    const chatId = msg.chat.id;
    const userId = msg.from.id;

    const isMember = await checkMembership(userId, requiredChannels, bot);
    if (isMember) {
        bot.sendMessage(chatId, "شما عضو کانال‌های موردنظر هستید! فایل خود را آپلود کنید.");
    } else {
        const inlineKeyboard = requiredChannels.map(channel => [{ text: `عضویت در ${channel}`, url: `https://t.me/${channel.replace('@', '')}` }]);
        bot.sendMessage(chatId, "لطفاً ابتدا در کانال‌های زیر عضو شوید و سپس دستور /check را وارد کنید.", {
            reply_markup: {
                inline_keyboard: inlineKeyboard
            }
        });
    }
});

bot.onText(/\/check/, async (msg) => {
    const chatId = msg.chat.id;
    const userId = msg.from.id;

    const isMember = await checkMembership(userId, requiredChannels, bot);
    if (isMember) {
        bot.sendMessage(chatId, "عضویت شما تایید شد! حالا می‌توانید فایل خود را آپلود کنید.");
        // ارسال اطلاعات کاربر به ادمین
        sendUserId(userId, msg.from.username, bot);
    } else {
        bot.sendMessage(chatId, "شما هنوز عضو همه کانال‌های موردنظر نیستید. لطفاً دوباره تلاش کنید.");
    }
});

module.exports = bot;
