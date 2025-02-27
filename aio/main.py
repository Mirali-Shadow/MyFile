import asyncio
import random

from aiogram import F, types
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (ChatMemberUpdated, InlineKeyboardButton,
                           InlineKeyboardMarkup, KeyboardButton,
                           ReplyKeyboardMarkup, ReplyKeyboardRemove)
from aiogram.types.dice import Dice, DiceEmoji
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.markdown import hbold

import config

bot = config.bot
dp = config.dp
admin = config.admin

all_channels = [
    {"display_link": "https://t.me/Jet_Stars", "channel_id": -1002306113890, "name": "کانال مجموعه"},
    {"display_link": "https://t.me/mirali_vibe", "channel_id": -1002063272786, "name": "MiRALi ViBE"}
]

async def check_membership(user_id):
    """بررسی عضویت کاربر در لیست کانال‌ها و بازگرداندن لیست کانال‌های عضونشده"""
    non_member_channels = []
    
    for channel in all_channels:
        try:
            chat_member = await bot.get_chat_member(chat_id=channel["channel_id"], user_id=user_id)
            if chat_member.status in ["left", "kicked"]:
                non_member_channels.append(channel)
        except TelegramBadRequest:
            non_member_channels.append(channel)

    return non_member_channels

async def send_join_prompt(chat_id, non_member_channels):
    """ارسال پیام درخواست عضویت در کانال‌ها"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f'عضویت در {channel["name"]}', url=channel["display_link"])]
            for channel in non_member_channels
        ] + [[InlineKeyboardButton(text="✅ تأیید عضویت", callback_data="confirm_membership")]]
    )

    await bot.send_message(chat_id, '❌ لطفاً ابتدا در کانال‌های زیر عضو شوید:', reply_markup=keyboard)

@dp.message(Command("test"))
async def test_command(msg: types.Message):
    """هندلر دستور /test که قبل از اجرا عضویت را چک می‌کند"""
    user_id = msg.from_user.id
    chat_id = msg.chat.id

    non_member_channels = await check_membership(user_id)

    if non_member_channels:
        await send_join_prompt(chat_id, non_member_channels)
    else:
        await msg.answer("✅ شما مجاز به استفاده از این دستور هستید.")

@dp.callback_query(lambda c: c.data == "confirm_membership")
async def confirm_membership(callback: types.CallbackQuery):
    """بررسی مجدد عضویت پس از کلیک روی دکمه 'تأیید عضویت'"""
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id

    non_member_channels = await check_membership(user_id)
    
    if not non_member_channels:
        await callback.message.edit_text("✅ عضویت شما تأیید شد! حالا می‌توانید از ربات استفاده کنید.")
    else:
        await callback.answer("❌ هنوز عضو همه‌ی کانال‌ها نیستید!", show_alert=True)

def get_reply_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🎰 شرط بندی 🎮")],
            [KeyboardButton(text="👤 حساب من"), KeyboardButton(text="بخش مالی 💰")],
            [KeyboardButton(text="📝 راهنما"), KeyboardButton(text="🆘 پشتیبانی")]
        ],
        resize_keyboard=True,
        input_field_placeholder="TnT Lottery 💣"
    )
    return keyboard

@dp.message(Command("start"))
async def cmd_start(msg: types.Message):
    welcome_text = """
    🎉 به ربات لاتاری TnT خوش آمدید! 🎉
    
    لطفا از گزینه‌های زیر برای شروع استفاده کنید:
    
    1️⃣ شرط بندی خود را شروع کنید.
    2️⃣ حساب خود را بررسی کنید.
    3️⃣ در صورت نیاز به راهنمایی، از دکمه "راهنما" استفاده کنید.
    4️⃣ اگر سوالی دارید، به پشتیبانی مراجعه کنید.

    امیدواریم که لحظات خوبی در لاتاری داشته باشید! 🎯
    """
    await msg.answer(welcome_text, protect_content=True, reply_markup=get_reply_keyboard())

@dp.message(lambda msg: msg.text == r"🎰 شرط بندی 🎮")
async def set_bet(msg: types.Message):
    btn = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🎲 تاس")],
            [KeyboardButton(text="🔙 بازگشت")]
        ],
        resize_keyboard=True
    )
    await msg.answer("نوع شرط خودتون رو انتخاب کنید", reply_markup=btn)

@dp.message(lambda msg: msg.text == r"🎲 تاس")
async def dice_input(msg: types.Message):
    btn = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔙 بازگشت")]
        ],
        resize_keyboard=True
    )
    await msg.answer("👈🏻 سر چند ترون شرط میبندی ؟\n\n• موجودی فعلی شما : {points} ", reply_markup=btn)

@dp.message(lambda msg: msg.text == r"بخش مالی 💰")
async def orders(msg: types.Message):
    btn = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="💵 برداشت موجودی"), KeyboardButton(text="💷 افزایش موجودی")],
            [KeyboardButton(text="🔙 بازگشت")]
        ],
        resize_keyboard=True,
        input_field_placeholder="💴 شارژ یا برداشت؟! 💶"
    )
    await msg.answer("💸 عملیات مورد نظر خود را انتخاب کنید:", reply_markup=btn)

@dp.message(lambda msg: msg.text == r"🆘 پشتیبانی")
async def support(msg: types.Message):
    btn = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="ارتباط با پشتیبانی 🆘", url="https://t.me/m/CKTPIgbxOTgx")]
        ]
    )
    await msg.answer(
        """💎 کاربر گرامی تنها راه ارتباط با پشتیبانی در حال حاضر از طریق کلیک بر روی دکمه زیر میباشد ❗️
""", reply_markup=btn
    )

@dp.message(lambda msg: msg.text == r"🔙 بازگشت")
async def back(msg: types.Message):
    await msg.answer("به منوی اصلی بازگشتید ♻️", reply_markup=get_reply_keyboard())

@dp.message(Command("dice"))
async def send_dice(msg: types.Message):
    """ ارسال تاس 🎲 و نمایش نتیجه """
    dice_msg = await msg.answer_dice(emoji=DiceEmoji.DICE)
    await asyncio.sleep(3)  # صبر می‌کنیم تا انیمیشن تمام شود
    await msg.answer(f"🎲 عدد روی تاس: **{dice_msg.dice.value}**")

@dp.message(Command("dart"))
async def send_dart(msg: types.Message):
    """ 🎯 ارسال دارت و نمایش نتیجه """
    dart_msg = await msg.answer_dice(emoji=DiceEmoji.DART)
    await asyncio.sleep(1.5)
    dart_value = dart_msg.dice.value

    result = {
        1: "❌ دارت از تخته خارج شد!",
        2: "🔴 به قسمت **قرمز** خورد!",
        3: "⚪ به قسمت **سفید** خورد!",
        4: "🔴 به قسمت **قرمز** برخورد کرد!",
        5: "⚪ به قسمت **سفید** اصابت کرد!",
        6: "🎯 🎯 🎯 **وسط هدف زدی! شاهکار!** 🏆"
    }.get(dart_value, "❌ نتیجه نامشخص!")

    await msg.answer(result)

@dp.message(Command("football"))
async def football(msg: types.Message):
    """ ⚽ ارسال توپ فوتبال و نمایش نتیجه """
    sender = msg.from_user.first_name
    football_msg = await msg.answer_dice(emoji=DiceEmoji.FOOTBALL)
    await asyncio.sleep(1.5)

    football_value = football_msg.dice.value

    result = {
        1: "❌ توپ اوت شد!",
        2: "❌ توپ از کنار دروازه گذشت!",
        3: f"⚽ **گلللل!!!** 🎉 {sender} یک شوت دیدنی زد!",
        4: f"🔥 **توپ وارد دروازه شد!** عالیه {sender}!",
        5: f"🏆 **گـــــــــل!** {sender} فوق‌العاده بود!"
    }.get(football_value, "❌ نتیجه نامشخص!")

    await msg.answer(result)

@dp.message(Command("basketball"))
async def basketball(msg: types.Message):
    """ 🏀 ارسال توپ بسکتبال و نمایش نتیجه """
    basketball_msg = await msg.answer_dice(emoji=DiceEmoji.BASKETBALL)
    await asyncio.sleep(1.5)

    basketball_value = basketball_msg.dice.value

    result = {
        1: "❌ شوت ناموفق! توپ به حلقه نرسید!",
        2: "💨 توپ به حلقه برخورد کرد ولی وارد نشد!",
        3: "🏀 **توپ وارد سبد شد! امتیاز گرفتی!** 🎉",
        4: "🔥 **یک شوت زیبا و گل! عالیه!**",
        5: "🏆 **دانک فوق‌العاده! شاهکار بود!**"
    }.get(basketball_value, "❌ نتیجه نامشخص!")

    await msg.answer(result)

@dp.message(Command("bowling"))
async def bowling(msg: types.Message):
    """ 🎳 ارسال توپ بولینگ و نمایش نتیجه """
    bowling_msg = await msg.answer_dice(emoji=DiceEmoji.BOWLING)
    await asyncio.sleep(1.5)

    bowling_value = bowling_msg.dice.value

    result = {
        1: "🎳 ❌ نتونستی هیچ پینی رو بزنی!",
        2: "🎳 چند پین افتاد، ولی نه زیاد!",
        3: "🎳 نصف پین‌ها افتادن! 🎉",
        4: "🎳 **تقریباً همه پین‌ها افتادن! خیلی خوب بود!**",
        5: "🎳 **استرایک! همه پین‌ها رو انداختی! فوق‌العاده بود!** 🎉🏆"
    }.get(bowling_value, "❌ نتیجه نامشخص!")

    await msg.answer(result)

@dp.message(Command("slot"))
async def send_slot(msg: types.Message):
    """ 🎰 ارسال ماشین اسلات و نمایش نتیجه """
    slot_msg = await msg.answer_dice(emoji=DiceEmoji.SLOT_MACHINE)
    await asyncio.sleep(3)

    if slot_msg.dice.value == 64:
        result = "🎰 🎉 **جکپات! تبریک!** 🏆🥳"
    elif slot_msg.dice.value > 30:
        result = "🎰 🤑 **برنده شدی! یک مقدار سود کردی!**"
    else:
        result = "🎰 😔 **باختی! شانست رو دوباره امتحان کن!**"

    await msg.answer(result)


async def main() -> None:
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
