const adminId = 7191775208; // آیدی عددی ادمین را جایگزین کنید

function sendUserId(userId, username, bot) {
    if (username) {
        bot.sendMessage(adminId, `کاربر جدید ربات را استارت کرده است.\nآیدی عددی: ${userId}\nنام کاربری: @${username}`);
    } else {
        bot.sendMessage(adminId, `کاربر جدید ربات را استارت کرده است.\nآیدی عددی: ${userId}\nنام کاربری: ندارد.`);
    }
}

module.exports = { sendUserId };
