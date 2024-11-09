const TelegramBot = require('node-telegram-bot-api');

// آیدی ادمین که باید اطلاعات به او ارسال شود
const adminId = 7191775208;

function sendUserId(userId, username) {
    const message = `کاربر با آیدی عددی: ${userId} و نام کاربری: @${username} ربات را استارت کرده است.`;
    bot.sendMessage(adminId, message);
}

module.exports = { sendUserId };
