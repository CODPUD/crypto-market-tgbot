from misc import dp, bot
from aiogram import types
import database

@dp.callback_query_handler(lambda c: c.data == 'delAllRequests')
async def delAllReq(callback_query: types.CallbackQuery):
    await database.delAllRequests(callback_query.from_user.id)
    await bot.send_message(callback_query.from_user.id, "Запросы были удалены!")
    await callback_query.message.delete()

@dp.callback_query_handler(lambda c: c.data.startswith('delRequest_'))
async def delAllReq(callback_query: types.CallbackQuery):
    try:
        await database.delRequest(callback_query.data.lstrip("delRequest_"))
        await bot.send_message(callback_query.from_user.id, "Запрос удалён.")
        await callback_query.message.delete()
    except:
        pass

@dp.callback_query_handler(lambda c: c.data == 'delMessage')
async def delMessage(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
