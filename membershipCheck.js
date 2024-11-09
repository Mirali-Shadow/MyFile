const tgbotapi = require('node-telegram-bot-api');

module.exports = {
    check: async function(userID, requiredChannels, bot) {
        for (let i = 0; i < requiredChannels.length; i++) {
            try {
                const chatMember = await bot.getChatMember(requiredChannels[i], userID);
                if (chatMember.status !== 'member' && chatMember.status !== 'administrator' && chatMember.status !== 'creator') {
                    return false; // اگر عضو نباشد
                }
            } catch (err) {
                console.log('Error checking membership: ', err);
                return false; // اگر خطایی رخ دهد
            }
        }
        return true; // اگر در همه کانال‌ها عضو باشد
    }
};
