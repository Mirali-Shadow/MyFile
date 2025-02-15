from telethon import events, Button
from telethon import Button, events
from telethon.tl import functions, types
from telethon.tl.functions.messages import SendReactionRequest
from telethon.tl.types import ReactionEmoji, ReactionPaid

import config

bot = config.bot

all_channels = [
    {"display_link": "https://t.me/Jet_Stars", "channel_id": "-1002306113890", "name": "کانال مجموعه"},
    {"display_link": "https://t.me/CryptoTacticians", "channel_id": "-1002063272786", "name": "Crypto Tactician"}
]
# 1001431076863  -  miox


async def check_membership(user_id):
    non_member_channels = []
    
    for channel in all_channels:
        try:
            result = await bot(functions.channels.GetParticipantRequest(
                channel=types.PeerChannel(int(channel["channel_id"])), 
                participant=user_id
            ))
        except Exception:
            non_member_channels.append(channel)

    return non_member_channels

async def send_join_prompt(user_id, chat_id):
    non_member_channels = await check_membership(user_id)

    if not non_member_channels:
        await bot.send_message(chat_id, '✅ عضویت شما در تمام کانال‌ها تأیید شد!\nمجددا دستور خودتون رو بفرستید')
        return

    buttons = [[Button.url(f'عضویت در {channel["name"]}', url=channel["display_link"])] for channel in non_member_channels]
    buttons.append([Button.inline('✅ تأیید عضویت', b'confirm_membership')])
    
    await bot.send_message(chat_id, '❌ لطفاً ابتدا در کانال‌های زیر عضو شوید:', buttons=buttons)
