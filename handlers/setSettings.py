from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from misc import dp, bot
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import req
import markup
from aiogram.dispatcher.filters import Text
import database
from config import admins

available_valper = ['Процент', 'Значение']
available_platform = ['Mercuryo', 'Banxa', 'Koinal']
available_crypto = []
available_fiat = []

class SetValPer(StatesGroup):
    valper = State()
    platform = State()
    crypto = State()
    fiat = State()
    range = State()

@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='Отменить запрос', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('Запрос отменён.', reply_markup=markup.markupMainMenu())

@dp.message_handler(lambda message: message.text == "Уст. значение\процент", state='*')
async def ValPer(message: types.Message):
    if message.from_user.id in admins:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        for button in available_valper:
            keyboard.insert(button)
        keyboard.add(KeyboardButton("Отменить запрос"))
        await bot.send_message(message.from_user.id, "Установить: ", reply_markup=keyboard)
        await SetValPer.valper.set()
    else:
        await message.answer('У вас нет доступа!')

@dp.message_handler(state=SetValPer.valper, content_types=types.ContentTypes.TEXT)
async def setValPer(message: types.Message, state: FSMContext):
    if message.text not in available_valper:
        await message.reply("Пожалуйста, выберите тип, используя клавиатуру ниже.")
        return
    await state.update_data(valper=message.text)

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for button in available_platform:
        keyboard.insert(KeyboardButton(button))
    keyboard.add(KeyboardButton("Отменить запрос"))
    await SetValPer.next()
    await bot.send_message(message.from_user.id, 'Выберите площадку: ', reply_markup=keyboard)

@dp.message_handler(state=SetValPer.platform, content_types=types.ContentTypes.TEXT)
async def setPlatform(message: types.Message, state: FSMContext):
    if message.text not in available_platform:
        await message.reply("Пожалуйста, выберите площадку, используя клавиатуру ниже.")
        return
    await state.update_data(platform=message.text)

    available_crypto.clear()
    buttons = None
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    if message.text == "Mercuryo":
        buttons = await req.getAllCryptoMercuryo()
    elif message.text == "Banxa":
        buttons = await req.getAllCryptoBanxa()
    elif message.text == "Koinal":
        buttons = ["BTC", "ETH", "LTC", "BCH", "XRP"]

    for button in buttons:
        available_crypto.append(button)
        keyboard.insert(KeyboardButton(button))
    keyboard.add(KeyboardButton("Отменить запрос"))
    await SetValPer.next()
    await bot.send_message(message.from_user.id, 'Выберите крипту: ', reply_markup=keyboard)

@dp.message_handler(state=SetValPer.crypto, content_types=types.ContentTypes.TEXT)
async def setCrypto(message: types.Message, state: FSMContext):
    if message.text not in available_crypto:
        await message.reply("Пожалуйста, выберите крипту, используя клавиатуру ниже.")
        return
    await state.update_data(crypto=message.text)

    available_fiat.clear()
    buttons = None
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    temp_data = await state.get_data()

    if(temp_data['platform'] == 'Mercuryo'):
        buttons = await req.getAllFiatMercuryo()
    elif (temp_data['platform'] == 'Banxa'):
        buttons = await req.getAllFiatBanxa()
    elif (temp_data['platform'] == 'Koinal'):
        buttons = ["USD"]

    for button in buttons:
        available_fiat.append(button)
        keyboard.insert(KeyboardButton(button))
    keyboard.add(KeyboardButton("Отменить запрос"))
    await SetValPer.next()
    await bot.send_message(message.from_user.id, 'Выберите валюту: ', reply_markup=keyboard)


@dp.message_handler(state=SetValPer.fiat, content_types=types.ContentTypes.TEXT)
async def setFiat(message: types.Message, state: FSMContext):
    if message.text not in available_fiat:
        await message.reply("Пожалуйста, выберите валюту, используя клавиатуру ниже.")
        return
    await state.update_data(fiat=message.text)

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Отменить запрос"))

    await SetValPer.next()
    await bot.send_message(message.from_user.id, "Отправьте диапазон: \n<b>Пример: </b><code>5 100</code>", reply_markup=keyboard)

@dp.message_handler(state=SetValPer.range, content_types=types.ContentTypes.TEXT)
async def setFiat(message: types.Message, state: FSMContext):
    temp_data = message.text.split(" ")
    try:
        if float(temp_data[0]) and float(temp_data[1]):
            if float(temp_data[1]) > float(temp_data[0]):
                pass
            else:
                await message.answer("Второй лимит должен быть больше чем первый!\n<b>Пример: </b><code>5 100</code>")
                return
    except:
        await message.answer("Введите только число\n<b>Пример: </b><code>5 100</code>")
        return

    data = await state.get_data()
    if (data['platform'] == "Mercuryo"):
        data["rate"] = await req.getRateMercuryo(data["crypto"], data["fiat"])
    elif (data['platform'] == "Banxa"):
        data["rate"] = await req.getRateBanxa(data["crypto"], data["fiat"])
    elif (data['platform'] == 'Koinal'):
        data["rate"] = await req.getRateKoinal(data["crypto"])
    data["user_id"] = message.from_user.id
    data["range_from"] = temp_data[0]
    data["range_to"] = temp_data[1]
    await database.addRequest(data)
    await state.finish()
    await bot.send_message(message.from_user.id, 'Запрос установлен.', reply_markup=markup.markupMainMenu())