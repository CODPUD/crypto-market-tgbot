from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import requests
from config import *

def markupMainMenu():
    button1 = KeyboardButton("Курс Mercuryo")
    button2 = KeyboardButton("Курс Banxa")
    button6 = KeyboardButton("Курс Koinal")
    button3 = KeyboardButton("Уст. значение\процент")
    button4 = KeyboardButton("Все запросы")
    button5 = KeyboardButton("Удалить все запросы")
    button7 = KeyboardButton("BestChange")
    button8 = KeyboardButton("Сравнение курсов")
    markup = ReplyKeyboardMarkup([[button1, button2, button6], [button3], [button4, button5], [button7, button8]], resize_keyboard=True)
    return markup

def markupMercuryoGetCrypto():
    response = requests.get(linkMercuryo).json()
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    for currency in response["data"]["buy"]:
        markup.insert(KeyboardButton("|M| "+currency))
    markup.add(KeyboardButton("Назад"))
    return markup

def markupBanxaGetCrypto():
    response = requests.get(linkBanxa).json()
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)

    for i in response["RateTicker"]["data"]["rates"]:
        response = response["RateTicker"]["data"]["rates"][i]
        break

    for currency in response:
        markup.insert(KeyboardButton("|B| " + currency))
    markup.add(KeyboardButton("Назад"))

    return markup

def markupDelAllReq():
    button_row1 = InlineKeyboardButton('Да', callback_data='delAllRequests')
    button_row2 = InlineKeyboardButton('Отменить', callback_data='delMessage')
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(button_row1)
    markup.add(button_row2)
    return markup
