const Telegram = require('node-telegram-bot-api');

async function checkMembership(bot, chatId, channels) {
    for (let channel of channels) {
            try {
                        const memberStatus = await bot.getChatMember(channel, chatId);
                                    if (memberStatus.status !== 'member' && memberStatus.status !== 'administrator' && memberStatus.status !== 'creator') {
                                                    return false; // کاربر عضو نیست
                                                                }
                                                                        } catch (error) {
                                                                                    console.error(`خطا در چک کردن عضویت در ${channel}:`, error);
                                                                                                return false; // در صورت بروز خطا، فرض می‌کنیم که کاربر عضو نیست
                                                                                                        }
                                                                                                            }
                                                                                                                return true; // کاربر به تمامی کانال‌ها پیوسته است
                                                                                                                }

                                                                                                                module.exports = checkMembership;
                                                                                                                