const TelegramBot = require('node-telegram-bot-api');
const fs = require('fs');
const path = require('path');

// توکن ربات تلگرام خود را وارد کنید
const token = '6414679474:AAHBrTFt5sCbbudkXHu3JvPrR_Pj50T30qs';  // توکن ربات خود را وارد کنید
const bot = new TelegramBot(token, { polling: true });

// لیست کانال‌هایی که باید کاربر در آنها عضو باشد
const requiredChannels = ["@mirali_vibe", "@mirali_vibe"];

// ذخیره وضعیت کاربران
const userStatus = {};

// تابع بررسی عضویت در کانال‌ها
async function checkUserMembership(userID, bot) {
    for (let channel of requiredChannels) {
        try {
            const chatMember = await bot.getChatMember(channel, userID);
            if (chatMember.status !== "member" && chatMember.status !== "administrator" && chatMember.status !== "creator") {
                return false;
            }
        } catch (error) {
            console.error('Error checking membership:', error);
            return false;
        }
    }
    return true;
}

// پیام خوش‌آمدگویی و درخواست آیدی در /start
bot.onText(/\/start/, async (msg) => {
    const chatId = msg.chat.id;
    const userId = msg.from.id;
    const username = msg.from.username || 'unknown_user';

    // ذخیره وضعیت کاربر
    userStatus[chatId] = { verified: false };

    // ارسال پیام به ادمین که کاربر ربات را استارت کرده است
    bot.sendMessage(7191775208, `کاربر جدید با آیدی ${userId} و نام کاربری ${username} ربات را استارت کرده است.`);

    // بررسی عضویت کاربر در کانال‌ها
    const isMember = await checkUserMembership(userId, bot);
    if (!isMember) {
        bot.sendMessage(chatId, "لطفاً ابتدا در کانال‌های موردنظر عضو شوید.");
        return;
    }

    // تغییر وضعیت به تایید عضویت
    userStatus[chatId].verified = true;

    // ارسال پیام خوش‌آمدگویی
    bot.sendMessage(chatId, "خوش آمدید! لینک کاستوم خود را ارسال کنید.");

    // ارسال منو برای استارت مجدد
    bot.sendMessage(chatId, "برای استارت مجدد ربات، لطفاً /start را وارد کنید.");
});

// هندلر برای لینک کاستوم و ارسال فایل‌ها
bot.on('message', async (msg) => {
    const chatId = msg.chat.id;
    const userId = msg.from.id;
    const username = msg.from.username || 'unknown_user';

    // چک کردن وضعیت کاربر و ارسال درخواست آیدی اگر تأیید نشده است
    if (!userStatus[chatId]?.verified) {
        return bot.sendMessage(chatId, "لطفاً ابتدا عضویت خود را تأیید کنید.");
    }

    // بررسی اینکه آیا پیامی حاوی لینک است
    if (msg.text && msg.text.startsWith("http")) {
        // اینجا می‌توانید فایل‌های مختلف را ارسال کنید
        bot.sendDocument(chatId, "path/to/your/file1.pdf");
        bot.sendDocument(chatId, "path/to/your/file2.zip");

        // ارسال آیدی عددی و نام کاربری (username) به پی‌وی شما
        bot.sendMessage(7191775208, `کاربر با آیدی عددی ${userId} و نام کاربری @${username} لینک را ارسال کرد.`);
    }
});

// هندلر برای ارسال منو با گزینه‌های مختلف
bot.onText(/\/menu/, (msg) => {
    const chatId = msg.chat.id;
    const menuOptions = {
        reply_markup: {
            keyboard: [
                ['/start', '/menu'],
            ],
            resize_keyboard: true,
            one_time_keyboard: true
        }
    };
    bot.sendMessage(chatId, "لطفاً یک گزینه انتخاب کنید:", menuOptions);
});
