from aiogram import types
from req import *
from misc import bot, dp
import markup
from config import admins

@dp.message_handler(lambda message: message.text == "Курс Mercuryo")
async def sendWelcome(message: types.Message):
    if message.from_user.id in admins:
        await bot.send_message(message.from_user.id, f"<b>Mercuryo</b>\nВыберите валюту: ", reply_markup=markup.markupMercuryoGetCrypto())
    else:
        await message.answer('У вас нет доступа!')

@dp.message_handler(lambda message: message.text.startswith("|M| "))
async def sendWelcome(message: types.Message):
    if message.from_user.id in admins:
        msg = await getMerCurrentRate(message.text[4:])
        await bot.send_message(message.from_user.id, msg)
    else:
        await message.answer('У вас нет доступа!')