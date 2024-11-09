async function checkMembership(userId, channels, bot) {
    for (let channel of channels) {
        try {
            const chatMember = await bot.getChatMember(channel, userId);
            if (chatMember.status !== 'member' && chatMember.status !== 'administrator' && chatMember.status !== 'creator') {
                return false;
            }
        } catch (error) {
            console.error(`خطا در بررسی عضویت در کانال ${channel}:`, error);
            return false;
        }
    }
    return true;
}

module.exports = { checkMembership };
