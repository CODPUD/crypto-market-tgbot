from misc import dp, bot
from aiogram import types
import markup
from req import *

@dp.message_handler(lambda message: message.text == "Курс Banxa")
async def sendWelcome(message: types.Message):
    if message.from_user.id in admins:
        await bot.send_message(message.from_user.id, f"<b>Banxa</b>\nВыберите валюту: ", reply_markup=markup.markupBanxaGetCrypto())
    else:
        await message.answer('У вас нет доступа!')

@dp.message_handler(lambda message: message.text.startswith("|B| "))
async def sendWelcome(message: types.Message):
    if message.from_user.id in admins:
        msg = await getBanxaCurrentRate(message.text[4:])
        await bot.send_message(message.from_user.id, msg)
    else:
        await message.answer('У вас нет доступа!')