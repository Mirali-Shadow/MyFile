const TelegramBot = require('node-telegram-bot-api');

// کانال‌هایی که باید بررسی شوند
const requiredChannels = ['@mirali_official', '@SHADOW_R3'];

// تابع بررسی عضویت
async function checkMembership(userId, bot) {
    for (let channel of requiredChannels) {
        try {
            const chatMember = await bot.getChatMember(channel, userId);
            if (chatMember.status !== 'member' && chatMember.status !== 'administrator' && chatMember.status !== 'creator') {
                return false;
            }
        } catch (error) {
            console.error(`خطا در بررسی عضویت در کانال ${channel}: `, error);
            return false;
        }
    }
    return true;
}

module.exports = { checkMembership };
