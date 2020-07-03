from aiogram.dispatcher import FSMContext

from config import API_TOKEN
import logging
import mssqldb

from aiogram import Bot, Dispatcher, executor, types

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nUse the command. /bo, /backoffice, /BO and last name to find when you came to work ' \nPowered by Dima.")

def auth(func):
    async def wrapper(message):
        if message['from']['id'] != 419859373:
            return await message.reply("Access Denied", reply=False)
        return await func(message)
    return wrapper


@dp.message_handler(state='*', commands=['bo','backoffice', 'BO', 'BO '])
async def last_coming(messsage: types.Message):
    name = messsage.get_args()
    if name is None:
        return
    last_coming = mssqldb.last_attendance_BO(name)
    if not last_coming:
        await messsage.reply("Сегодня еще никто не прищел", reply=False)
        return
    last_coming_row = [
        f"{row['hhmmss']}"
        f" ({row['Name']})"
        for row in last_coming]
    answer_message = 'Приход за "day":\n\n*' + "\n\n*".join(last_coming_row)
    await messsage.reply(answer_message, reply=False)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
