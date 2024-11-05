const TelegramBot = require('node-telegram-bot-api');

// توکن ربات خود را از BotFather وارد کنید
const token = '6414679474:AAHBrTFt5sCbbudkXHu3JvPrR_Pj50T30qs'; // توکن ربات خود را وارد کنید
const bot = new TelegramBot(token, { polling: true });

// نام کانال‌های خود را اینجا وارد کنید
const CHANNELS = ['@MIRALI_VIBE', '@SHADOW_R3'];
const CHANNELS_LINKS = ['https://t.me/MIRALI_VIBE', 'https://t.me/SHADOW_R3'];

// اطلاعات آهنگ‌ها
const albums = [
    {
        title: "آلبوم 1",
        tracks: [
            { title: "آهنگ 1", url: "https://github.com/Mirali-Shadow/MyFile/raw/refs/heads/main/Pishro%20-%20Tamum%20Shode%20(featuring%20Kamyar).mp3" },
            // { title: "آهنگ 2", url: "https://example.com/path/to/song2.mp3" },
            // { title: "آهنگ 3", url: "https://example.com/path/to/song3.mp3" }
        ]
    },
    {
        title: "آلبوم 2",
        tracks: [
            { title: "آهنگ 4", url: "https://example.com/path/to/song4.mp3" },
            { title: "آهنگ 5", url: "https://example.com/path/to/song5.mp3" },
            { title: "آهنگ 6", url: "https://example.com/path/to/song6.mp3" }
        ]
    }
];

// ارسال پیام شیشه‌ای
function sendGlassMessage(chatId, text) {
    const glassMessage = "💎 " + text + " 💎";
    bot.sendMessage(chatId, glassMessage);
}

// فرمان شروع ربات
bot.onText(/\/start/, (msg) => {
    const chatId = msg.chat.id;
    sendGlassMessage(chatId, "برای استفاده از ربات، لطفاً به دو کانال زیر ملحق شوید:\n" +
        "1. [کانال 1](" + CHANNELS_LINKS[0] + ")\n" +
        "2. [کانال 2](" + CHANNELS_LINKS[1] + ")\n\n" +
        "سپس بر روی /confirm کلیک کنید تا عضویت شما تایید شود.");
});

// بررسی عضویت کاربر
async function isUserMember(chatId, channel) {
    try {
        const memberStatus = await bot.getChatMember(channel, chatId);
        return memberStatus.status === 'member' || memberStatus.status === 'administrator';
    } catch (error) {
        return false; // کاربر عضو نیست یا خطایی رخ داده است
    }
}

// فرمان تایید عضویت
bot.onText(/\/confirm/, async (msg) => {
    const chatId = msg.chat.id;
    let allMembers = true;

    for (let i = 0; i < CHANNELS.length; i++) {
        const channel = CHANNELS[i];
        const isMember = await isUserMember(chatId, channel);
        if (!isMember) {
            bot.sendMessage(chatId, "شما هنوز عضو کانال " + CHANNELS_LINKS[i] + " نیستید.");
            allMembers = false;
            break;
        }
    }

    if (allMembers) {
        bot.sendMessage(chatId, "شما عضو هستید! حالا می‌توانید آلبوم‌ها را مشاهده کنید.");
        showAlbums(chatId);
    }
});

// نمایش پنل کاربری با آهنگ‌ها
function showAlbums(chatId) {
    albums.forEach(album => {
        let message = "🎶 " + album.title + " 🎶\n";
        album.tracks.forEach((track, index) => {
            message += `${index + 1}. ${track.title} - /play${index + 1}\n`;
        });
        sendGlassMessage(chatId, message);
    });
}

// فرمان پخش آهنگ
bot.onText(/\/play(\d+)/, (msg, match) => {
    const chatId = msg.chat.id;
    const trackIndex = parseInt(match[1]) - 1; // تبدیل به ایندکس صفر

    let found = false;
    albums.forEach(album => {
        if (trackIndex < album.tracks.length) {
            found = true;
            const track = album.tracks[trackIndex];
            bot.sendAudio(chatId, track.url, { caption: `در حال پخش: ${track.title}` });
        }
    });

    if (!found) {
        bot.sendMessage(chatId, "آهنگ مورد نظر یافت نشد.");
    }
});
