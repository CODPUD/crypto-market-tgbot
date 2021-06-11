from aiogram import types
from .bestChange_requests import getBestChange
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from misc import bot, dp
from config import buttonsBestChange, admins

@dp.message_handler(lambda message: message.text == "BestChange")
async def BestChanges(message: types.Message):
    if message.from_user.id in admins:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
        for button in buttonsBestChange:
            keyboard.insert("B-"+button)
        keyboard.add(KeyboardButton("Назад"))
        await bot.send_message(message.chat.id, "Выберите крипту: ", reply_markup=keyboard)
    else:
        await message.answer('У вас нет доступа!')

@dp.message_handler(lambda message: message.text.startswith("B-"))
async def sendWelcome(message: types.Message):
    try:
        await message.answer("Ожидайте...")
        if message.from_user.id in admins:
            data = await getBestChange(buttonsBestChange[message.text[2:]])
            msg = f"Обменник: <b>{data['name']}</b>\n" \
                  f"Отдаете: <b>{data['rate']}</b>\n" \
                  f"Резерв: <b>{data['reserve']}</b>\n" \
                  f"Отзывы: <b>{data['feedback']}</b>"

            keyboard = InlineKeyboardMarkup()
            keyboard.add(InlineKeyboardButton("Перейти на сайт", data['link']))
            keyboard.add(InlineKeyboardButton('Скрыть', callback_data='delMessage'))
            await bot.send_message(message.from_user.id, msg, reply_markup=keyboard)
        else:
            await message.answer('У вас нет доступа!')
    except Exception as ex:
        print(ex)