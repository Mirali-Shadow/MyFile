from telethon import TelegramClient, events
from config1 import api_id , api_hash

from asyncio import sleep

from telethon.tl.custom.message import Message



client = TelegramClient('bot_session', api_id=api_id, api_hash=api_hash)


@client.on(events.NewMessage(pattern=r'/start'))
async def start(event: Message):
    msg: Message = await client.send_message(entity=event.chat_id, message='سلام مسلمون خر', reply_to=event.id)
    await sleep(2)
    await client.edit_message(entity=event.chat_id, message=msg.id, text='ببخشید مسلمون نیستی انگار')
    await sleep(2)
    await client.delete_messages(entity=msg.chat_id, message_ids=msg.id);
    await sleep(2)
    fwrd = await client.forward_messages(entity=event.chat_id, messages=100, from_peer='@mirali_vibe')
    await sleep(2)
    await client.pin_message(entity=event.chat_id, message=fwrd)
    await sleep(2)
    await client.unpin_message(entity = msg.chat_id, message=fwrd)
    await sleep(2)



client.start(bot_token='7939330356:AAGuiK7SzjAsNKETYyMp3CI_KOKi1muyeRY')
client.run_until_disconnected()