from aiogram import executor
from misc import dp, bot
import handlers
import asyncio
import req
import database
from config import comission, interval
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# 0 - id
# 1 - valper
# 2 - platform
# 3 - crypto
# 4 - fiat
# 5 - user id
# 6 - previous rate
# 7 - range from
# 8 - range to

msg = "<b>{8} {0}</b> >> <b>{1}</b>\n" \
      "Диапазон: <b>{2} - {3} {4}</b>\n" \
      "Предыдущий: {5}\n" \
      "Текущий: {6}\n" \
      "Разница: <b>{7}{4}</b>"

async def updateMercuryoRates(data):
    try:
        rates = await req.getDataMercuryo()
        rate = round(float(rates[data[3]][data[4]]), 2)
        await database.updateRate(data[0], rate)
    except Exception as ex:
        print(ex)

async def updateBanxaRates(data):
    try:
        rates = await req.getDataBanxa()
        rate = round(float(rates["rates"][data[4]][data[3]]["Value"])*comission, 2)
        await database.updateRate(data[0], rate)
    except Exception as ex:
        print(ex)

async def updateKoinalRates(data):
    try:
        rate = await req.getRateKoinal(data[3])
        await database.updateRate(data[0], rate)
    except Exception as ex:
        print(ex)

async def updateAllRates():
    try:
        bigData = await database.getAllRequests()
        for data in bigData:
            if data[2] == "Mercuryo":
                await updateMercuryoRates(data)
            elif data[2] == "Banxa":
                await updateBanxaRates(data)
            elif data[2] == "Koinal":
                await updateKoinalRates(data)
    except Exception as ex:
        print(ex)

async def difByValue(prev, curr):
    return round(curr - prev, 2)

async def difByPercentage(prev, cur):
    return round((cur/prev-1)*100, 2)

async def getDifference(data, ratesM ,ratesB):
    try:
        current_value = None
        if data[2] == "Mercuryo":
            current_value = round(float(ratesM[data[3]][data[4]]), 2)
        elif data[2] == "Banxa":
            current_value = round(float(ratesB["rates"][data[4]][data[3]]["Value"])*comission, 2)
        elif data[2] == "Koinal":
            current_value = float(await req.getRateKoinal(data[3]))

        previous_value = data[6]
        range_from = data[7]
        range_to = data[8]

        if(data[1] == "Значение"):
            difference = await difByValue(previous_value, current_value)
            if(difference!=0) and ((range_from < difference and difference < range_to) or (0-range_to < difference and difference < 0-range_from)):
                try:
                    markup = InlineKeyboardMarkup(row_width=2)
                    button_row1 = InlineKeyboardButton('Скрыть', callback_data='delMessage')
                    button_row2 = InlineKeyboardButton('Удалить запрос', callback_data=f'delRequest_{data[0]}')
                    markup.add(button_row1)
                    markup.add(button_row2)
                    await database.updateRate(data[0], current_value)
                    await bot.send_message(data[5], msg.format(data[3], data[4], range_from, range_to, data[4], previous_value, current_value, difference, data[2]), reply_markup=markup)
                except:
                    pass
        elif(data[1] == "Процент"):
            difference = await difByPercentage(previous_value, current_value)
            if(difference!=0) and ((range_from < difference and difference < range_to) or (0-range_to < difference and difference < 0-range_from)):
                try:
                    markup = InlineKeyboardMarkup(row_width=2)
                    button_row1 = InlineKeyboardButton('Скрыть', callback_data='delMessage')
                    button_row2 = InlineKeyboardButton('Удалить запрос', callback_data=f'delRequest_{data[0]}')
                    markup.add(button_row1)
                    markup.add(button_row2)
                    await database.updateRate(data[0], current_value)
                    await bot.send_message(data[5], msg.format(data[3], data[4], range_from, range_to, "%", previous_value, current_value, difference, data[2]), reply_markup=markup)
                except:
                    pass
    except Exception as ex:
        print(ex)

async def signal():
    await updateAllRates()
    while 1:
        try:
            await asyncio.sleep(interval)
            bigData = await database.getAllRequests()
            ratesM = await req.getDataMercuryo()
            ratesB = await req.getDataBanxa()

            for data in bigData:
                    await getDifference(data, ratesM, ratesB)
        except:
            pass


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(signal())
    executor.start_polling(dp, skip_updates=True)