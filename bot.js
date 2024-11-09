const TelegramBot = require('node-telegram-bot-api');
const { checkMembership } = require('./membershipCheck'); // وارد کردن تابع بررسی عضویت
const { sendUserId } = require('./idSend'); // وارد کردن تابع ارسال آیدی
const fs = require('fs');
const path = require('path');

// توکن ربات تلگرام خود را وارد کنید
const token = '6414679474:AAHBrTFt5sCbbudkXHu3JvPrR_Pj50T30qs';
const bot = new TelegramBot(token, { polling: true });

// پوشه‌ای برای ذخیره فایل‌های آپلود شده
const uploadDir = path.join(__dirname, 'uploads');
const logFilePath = path.join(__dirname, 'uploads_log.txt'); // فایل لاگ برای ذخیره تاریخچه آپلودها

// اگر پوشه 'uploads' وجود ندارد، آن را ایجاد می‌کنیم
if (!fs.existsSync(uploadDir)) {
    fs.mkdirSync(uploadDir);
}

// ذخیره وضعیت کاربران
const userStatus = {};

// پیام خوش‌آمدگویی و درخواست آیدی در /start
bot.onText(/\/start/, (msg) => {
    const chatId = msg.chat.id;
    userStatus[chatId] = { verified: false }; // وضعیت اولیه کاربر
    bot.sendMessage(chatId, `خوش آمدید! لطفاً ابتدا آیدی تلگرام خود را مانند @example_telegram ارسال کنید تا بتوانید فایل آپلود کنید.`);
});

// هندلر برای بررسی آیدی ارسالی کاربر
bot.onText(/^@([a-zA-Z0-9_]{5,})$/, (msg) => {
    const chatId = msg.chat.id;
    
    // اگر کاربر تأیید نشده، آیدی او را تأیید کنیم
    if (!userStatus[chatId]?.verified) {
        userStatus[chatId].verified = true; // تأیید آیدی
        bot.sendMessage(chatId, "آیدی شما تأیید شد! حالا می‌توانید فایل‌ها را آپلود کنید.");
    } else {
        bot.sendMessage(chatId, "شما قبلاً تأیید شده‌اید و می‌توانید فایل آپلود کنید.");
    }
});

// هندلر برای دریافت فایل‌ها
bot.on('message', async (msg) => {
    const chatId = msg.chat.id;
    const username = msg.from.username || 'unknown_user'; // نام کاربری کاربر

    // چک کردن وضعیت کاربر و ارسال درخواست آیدی اگر تأیید نشده است
    if (!userStatus[chatId]?.verified) {
        return; // اگر کاربر تأیید نشده باشد، بدون ارسال پیام برمی‌گردد
    }

    // ادامه پردازش فایل‌ها فقط برای کاربران تأیید شده
    let fileId, fileName;
    if (msg.document) {
        fileId = msg.document.file_id;                     // اسناد
        fileName = msg.document.file_name || `file_${Date.now()}`; // نام فایل یا یک نام تصادفی
    } else if (msg.video) {
        fileId = msg.video.file_id;                        // ویدیو
        fileName = msg.video.file_name || `video_${Date.now()}`; // نام ویدیو یا یک نام تصادفی
    } else if (msg.audio) {
        fileId = msg.audio.file_id;                        // صوت
        fileName = msg.audio.file_name || `audio_${Date.now()}`; // نام صوت یا یک نام تصادفی
    } else if (msg.photo) {
        fileId = msg.photo[msg.photo.length - 1].file_id;  // عکس
        fileName = `photo_${Date.now()}.jpg`;              // چون عکس نام فایل ندارد
    } else {
        return bot.sendMessage(chatId, "لطفاً یک فایل معتبر (عکس، سند، ویدیو، صوت) ارسال کنید.");
    }

    try {
        // دانلود و ذخیره فایل با نام اصلی
        bot.downloadFile(fileId, uploadDir).then(filePath => {
            const originalFilePath = path.join(uploadDir, fileName);
            fs.rename(filePath, originalFilePath, (err) => {
                if (err) {
                    console.error('خطا در تغییر نام فایل:', err);
                    return bot.sendMessage(chatId, "مشکلی در ذخیره فایل شما به وجود آمد.");
                }

                // ذخیره اطلاعات آپلود در فایل لاگ
                const logEntry = `کاربر: ${username}, فایل: ${fileName}\n`;
                fs.appendFile(logFilePath, logEntry, (err) => {
                    if (err) {
                        console.error('خطا در نوشتن لاگ آپلود:', err);
                    }
                });

                // ارسال فایل و اطلاعات به ادمین
                sendUserId(chatId, username, fileName);
                bot.sendMessage(chatId, `فایل "${fileName}" با موفقیت آپلود شد \n برای ارسال فایل‌های بیشتر روی /start کلیک کنید!`);
            });
        });
    } catch (error) {
        console.error('خطا در دانلود فایل:', error);
        bot.sendMessage(chatId, "مشکلی در آپلود فایل شما به وجود آمد.");
    }
});

// هندلر برای ارسال آیدی و اطلاعات کاربر
bot.onText(/\/check/, (msg) => {
    const chatId = msg.chat.id;
    const userId = msg.from.id;
    const username = msg.from.username || 'نام کاربری ندارد';

    // ارسال اطلاعات به پیوی ادمین
    sendUserId(userId, username);

    bot.sendMessage(chatId, "اطلاعات شما ارسال شد.");
});
