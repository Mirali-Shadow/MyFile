const TelegramBot = require('node-telegram-bot-api');
const checkUserMembership = require('./checkMembership');

// توکن ربات و آی‌دی ادمین را تعریف کنید
const token = '6414679474:AAHBrTFt5sCbbudkXHu3JvPrR_Pj50T30qs';
const adminId = '7191775208';
const bot = new TelegramBot(token, { polling: true });

// کانال‌های مورد نیاز برای عضویت
const requiredChannels = ['@channel1', '@channel2'];

// ارسال پیام خوش‌آمدگویی و راستی‌آزمایی عضویت
bot.onText(/\/start/, async (msg) => {
    const chatId = msg.chat.id;
    const userId = msg.from.id;

    // ارسال آی‌دی کاربر به ادمین
    bot.sendMessage(adminId, `کاربر جدید با آیدی ${userId} ربات را استارت کرده است.`);

    // بررسی عضویت کاربر در کانال‌ها
    const isMember = await checkUserMembership(userId, requiredChannels, token);

    if (!isMember) {
        return bot.sendMessage(
            chatId,
            `لطفاً ابتدا در کانال‌های زیر عضو شوید:\n${requiredChannels.join('\n')}`
        );
    }

    // ایجاد منو و ارسال پیام خوش‌آمدگویی
    bot.sendMessage(chatId, "به ربات خوش آمدید! لینک کاستوم خود را بفرستید تا فایل‌های مرتبط ارسال شود.", {
        reply_markup: {
            keyboard: [['/start']],
            resize_keyboard: true,
            one_time_keyboard: true
        }
    });
});

// هندلر دریافت لینک کاستوم و ارسال فایل
bot.on('message', async (msg) => {
    const chatId = msg.chat.id;
    const userId = msg.from.id;

    if (msg.text.startsWith("http")) { // بررسی لینک کاستوم
        const isMember = await checkUserMembership(userId, requiredChannels, token);

        if (!isMember) {
            return bot.sendMessage(
                chatId,
                `لطفاً ابتدا در کانال‌های زیر عضو شوید:\n${requiredChannels.join('\n')}`
            );
        }

        // ارسال فایل‌های مرتبط با لینک (اینجا فایل‌ها ثابت هستند؛ شما می‌توانید فایل‌های متناسب با لینک را تنظیم کنید)
        bot.sendDocument(chatId, 'path/to/your/file1.pdf');
        bot.sendDocument(chatId, 'path/to/your/file2.zip');
    }
});
