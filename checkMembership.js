const axios = require('axios');

// تابع برای بررسی عضویت کاربر در کانال‌های خاص
async function checkUserMembership(userId, channels, botToken) {
    for (const channel of channels) {
        const url = `https://api.telegram.org/bot${botToken}/getChatMember?chat_id=${channel}&user_id=${userId}`;
        try {
            const response = await axios.get(url);
            const status = response.data.result.status;
            if (status !== 'member' && status !== 'administrator' && status !== 'creator') {
                return false; // کاربر عضو نیست
            }
        } catch (error) {
            console.error(`خطا در بررسی کانال ${channel}:`, error.message);
            return false; // در صورت خطا کاربر عضو در نظر گرفته نمی‌شود
        }
    }
    return true; // کاربر عضو تمام کانال‌ها است
}

module.exports = checkUserMembership;
