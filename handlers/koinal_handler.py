from aiogram import types
from req import *
from misc import bot, dp


@dp.message_handler(lambda message: message.text == "Курс Koinal")
async def sendWelcome(message: types.Message):
    if message.from_user.id in admins:
        msg = "<b>USD</b>\n<code>"
        data = await getDataKoinal()
        for crypto in data['rate']:
            msg += " | " + crypto + " | " + data['rate'][crypto] + "\n"
        msg += "</code>"
        await bot.send_message(message.from_user.id, msg)
    else:
        await message.answer('У вас нет доступа!')