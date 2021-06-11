from misc import dp, bot
from aiogram import types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
import markup
from config import admins

@dp.message_handler(commands="start")
async def sendWelcome(message: types.Message):
    if message.from_user.id in admins:
        await bot.send_message(message.from_user.id, f"Привет, {message.from_user.first_name}", reply_markup=markup.markupMainMenu())
    else:
        await message.answer('У вас нет доступа!', reply_markup=ReplyKeyboardMarkup([[KeyboardButton("id")]], resize_keyboard=True))