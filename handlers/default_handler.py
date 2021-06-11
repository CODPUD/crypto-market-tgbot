from misc import dp, bot
from aiogram import types
import markup
import database
from config import admins
from aiogram.types import  ReplyKeyboardMarkup, KeyboardButton

@dp.message_handler(lambda message: message.text == "Все запросы")
async def getAllRequests(message: types.Message):
    if message.from_user.id in admins:
        big_data = await database.getRequests(message.from_user.id)
        msgMer = "<b>Mercuryo</b>\n<code>"
        msgBan = "<b>Banxa</b>\n<code>"
        msgKoi = "<b>Koinal</b>\n<code>"
        for data in big_data:
            if data[2] == "Mercuryo":
                msgMer +=  data[1] + " | " + data[3] + " | " + data[4] + " | " + str(data[7]) + "-" + str(data[8]) + "\n"
            elif data[2] == "Banxa":
                msgBan +=  data[1] + " | " + data[3] + " | " + data[4] + " | " + str(data[7]) + "-" + str(data[8]) + "\n"
            elif data[2] == "Koinal":
                msgKoi +=  data[1] + " | " + data[3] + " | " + data[4] + " | " + str(data[7]) + "-" + str(data[8]) + "\n"
        msgMer += "</code>\n" + msgBan + "</code>\n" + msgKoi + "</code>"
        await bot.send_message(message.from_user.id, msgMer)
    else:
        await message.answer('У вас нет доступа!')

@dp.message_handler(lambda message: message.text == "Удалить все запросы")
async def delAllRequests(message: types.Message):
    if message.from_user.id in admins:
        await bot.send_message(message.from_user.id, "Вы точно хотите удалить все запросы ?", reply_markup=markup.markupDelAllReq())
    else:
        await message.answer('У вас нет доступа!')

@dp.message_handler(lambda message: message.text.lower() == "id")
async def sendId(message: types.Message):
    await message.answer("Ваш id: <code>" + str(message.from_user.id) + "</code>")

@dp.message_handler()
@dp.message_handler(lambda message: message.text == "Назад")
async def sendWelcome(message: types.Message):
    if message.from_user.id in admins:
        await bot.send_message(message.from_user.id, f"Меню: ", reply_markup=markup.markupMainMenu())
    else:
        await message.answer('У вас нет доступа!', reply_markup=ReplyKeyboardMarkup([[KeyboardButton("id")]], resize_keyboard=True))