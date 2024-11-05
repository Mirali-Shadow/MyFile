const TelegramBot = require('node-telegram-bot-api');

// توکن ربات خود را از BotFather وارد کنید
const token = '6414679474:AAHBrTFt5sCbbudkXHu3JvPrR_Pj50T30qs';
const bot = new TelegramBot(token, { polling: true });

// نام کانال‌های خود را اینجا وارد کنید
const CHANNELS = ['@MIRALI_VIBE', '@SHADOW_R3'];
const CHANNELS_LINKS = ['https://t.me/MIRALI_VIBE', 'https://t.me/SHADOW_R3'];

// هندلرهای دستورات
bot.onText(/\/start/, (msg) => {
    const chatId = msg.chat.id;
    bot.sendMessage(chatId, "به ربات ما خوش آمدید! برای کمک از /help استفاده کنید.");
});

bot.onText(/\/help/, (msg) => {
    const chatId = msg.chat.id;
    const helpText = "برای درخواست یک فایل، روی دکمه زیر کلیک کنید:\n" +
                     "فقط بر روی لینک ارائه شده کلیک کنید!";
    bot.sendMessage(chatId, helpText);
});

// تابع بررسی عضویت کاربر در کانال‌های مشخص شده
async function isUserMember(chatId, channel) {
    try {
        const memberStatus = await bot.getChatMember(channel, chatId);
        return memberStatus.status === 'member' || memberStatus.status === 'administrator';
    } catch (error) {
        return false; // کاربر عضو نیست یا خطایی رخ داده است
    }
}

// هندلر درخواست
bot.onText(/\/request/, async (msg) => {
    const chatId = msg.chat.id;
    let isMember = true;

    // بررسی عضویت برای هر کانال
    for (let channel of CHANNELS) {
        isMember = await isUserMember(channel, chatId);
        if (!isMember) {
            const index = CHANNELS.indexOf(channel);
            bot.sendMessage(chatId, "شما باید عضو کانال " + CHANNELS_LINKS[index] + " شوید تا به فایل‌ها دسترسی داشته باشید.");
            return;
        }
    }

    // اگر کاربر عضو همه کانال‌ها باشد
    const fileLink = "https://github.com/Mirali-Shadow/MyFile/raw/refs/heads/main/Pishro%20-%20Tamum%20Shode%20(featuring%20Kamyar).mp3"; // لینک فایل واقعی خود را وارد کنید
    bot.sendMessage(chatId, "شما عضو هستید! در اینجا فایل شما: " + fileLink);
});

// تابع پیام شیشه‌ای برای تمام مراحل
function sendGlassMessage(chatId, text) {
    const glassMessage = "💎 " + text + " 💎";
    bot.sendMessage(chatId, glassMessage);
}

// گوش دادن به اقدامات کاربر و ارائه پیام‌های شیشه‌ای
bot.on('message', (msg) => {
    const chatId = msg.chat.id;
    if (msg.text) {
        sendGlassMessage(chatId, "شما پیامی ارسال کردید: " + msg.text);
    }
});
