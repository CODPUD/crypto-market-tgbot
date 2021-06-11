from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from misc import dp, bot
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import req
import markup
from aiogram.dispatcher.filters import Text
from config import admins, comission, rounder

crypto_buttons = ['BTC', 'ETH']
fiat_buttons = ['RUB', 'USD']

class CryptoFiat(StatesGroup):
    crypto = State()
    fiat = State()

@dp.message_handler(Text(equals='Отменить сравнение', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('Сравнение отменено.', reply_markup=markup.markupMainMenu())

@dp.message_handler(lambda message: message.text == "Сравнение курсов", state="*")
async def Comaper(message: types.Message):
    if message.from_user.id in admins:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

        for button in crypto_buttons:
            keyboard.insert(button)
        keyboard.add(KeyboardButton("Отменить сравнение"))

        await bot.send_message(message.from_user.id, "Выберите крипту: ", reply_markup=keyboard)
        await CryptoFiat.crypto.set()
    else:
        await message.answer('У вас нет доступа!')

@dp.message_handler(state=CryptoFiat.crypto, content_types=types.ContentTypes.TEXT)
async def setValPer(message: types.Message, state: FSMContext):
    if message.text not in crypto_buttons:
        await message.reply("Пожалуйста, выберите крипту, используя клавиатуру ниже.")
        return
    await state.update_data(crypto=message.text)

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for button in fiat_buttons:
        keyboard.insert(KeyboardButton(button))
    keyboard.add(KeyboardButton("Отменить запрос"))
    await CryptoFiat.next()
    await bot.send_message(message.from_user.id, 'Выберите валюту: ', reply_markup=keyboard)

@dp.message_handler(state=CryptoFiat.fiat, content_types=types.ContentTypes.TEXT)
async def setFiat(message: types.Message, state: FSMContext):
    if message.text not in fiat_buttons:
        await message.reply("Пожалуйста, выберите валюту, используя клавиатуру ниже.")
        return
    await state.update_data(fiat=message.text)
    data = await state.get_data()
    await state.finish()

    await bot.send_message(message.from_user.id, 'Сравнение, ожидайте...', reply_markup=ReplyKeyboardRemove())
    await getMinRate(data, message.from_user.id)



async def getMinRate(data, user_id):
    rates = {}

    current_banxa = await req.getDataBanxa()
    current_banxa = round(float(current_banxa["rates"][data['fiat']][data['crypto']]["Value"]) * comission, 2)
    rates['banxa'] = current_banxa

    current_mercuryo = await req.getDataMercuryo()
    current_mercuryo = round(float(current_mercuryo[data['crypto']][data['fiat']]), 2)
    rates['mercuryo'] = current_mercuryo

    if data['fiat'] == "USD":
        current_koinal = await req.getDataKoinal()
        current_koinal = float(current_koinal['rate'][data['crypto']])
        rates['koinal'] = current_koinal

    platform = min(rates, key=rates.get)
    await bot.send_message(user_id, f"<b>{platform} {data['crypto']} >> {data['fiat']}</b>\nКурс: {rates[platform]} {data['fiat']}", reply_markup=markup.markupMainMenu())
