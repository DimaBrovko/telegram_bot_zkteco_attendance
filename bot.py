from config import API_TOKEN
import logging
import mssqldb
import re

from aiogram import Bot, Dispatcher, executor, types

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nUse the command. /att and last name to find when you came to work ' \nPowered by Dima.")

def auth(func):
    async def wrapper(message):
        if message['from']['id'] != 419859373:
            return await message.reply("Access Denied", reply=False)
        return await func(message)
    return wrapper


def parse_message():
    return


@dp.message_handler(state='*', commands=['att'])
async def last_coming(messsage: types.Message):
    name = messsage.get_args()
    massage_list = []
    for word in name.split():
        clear_words =""
        for letter in word:
                clear_words += letter
        massage_list.append(clear_words)
    print(massage_list)
    if massage_list is None:
        return
    last_coming = mssqldb.last_attendance_BO(massage_list)
    if not last_coming:
        await messsage.reply("No data", reply=False)
        return
    last_coming_row = [
        f"{row['day']}"
        f" / {row['hhmmss']}"
        f" ({row['Name']})"
        for row in last_coming]
    answer_message = 'Coming to work in:\n\n' + "\n\n*".join(last_coming_row)
    await messsage.reply(answer_message, reply=False)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
