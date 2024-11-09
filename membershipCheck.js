const { ChatMemberStatus } = require('node-telegram-bot-api');

// تابع برای بررسی عضویت کاربر در کانال
async function checkMembership(bot, chatId, channelUsername) {
    try {
        const member = await bot.getChatMember(channelUsername, chatId);
        if (member.status === ChatMemberStatus.MEMBER || member.status === ChatMemberStatus.ADMINISTRATOR || member.status === ChatMemberStatus.CREATOR) {
            return true;
        } else {
            return false;
        }
    } catch (error) {
        console.error('خطا در بررسی عضویت:', error);
        return false;
    }
}

module.exports = { checkMembership };
