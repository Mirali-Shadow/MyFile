const TelegramBot = require('node-telegram-bot-api');

// تابعی برای بررسی عضویت کاربر در یک کانال خاص
async function isUserMember(bot, channelId, userId) {
    try {
        const member = await bot.getChatMember(channelId, userId);
        return (member.status === 'member' || member.status === 'administrator' || member.status === 'creator');
    } catch (error) {
        console.log("خطا در بررسی عضویت:", error.message);
        return false;
    }
}

module.exports = { isUserMember };
