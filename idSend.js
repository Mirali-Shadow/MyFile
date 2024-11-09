const adminId = '7191775208'; // آیدی ادمین که اطلاعات باید به اون ارسال بشه

// تابع ارسال اطلاعات آیدی به ادمین
function sendUserId(userId, username, fileName = 'No file') {
    const message = `کاربر: ${username} \nآیدی کاربر: ${userId} \nفایل: ${fileName}`;
    bot.sendMessage(adminId, message);
}

module.exports = { sendUserId };
