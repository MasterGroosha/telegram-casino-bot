import logging
from aiogram import Bot, Dispatcher, executor, types
from os import getenv
from sys import exit

# Токен берётся из переменной окружения (можно задать через systemd unit)
token = getenv("BOT_TOKEN")
if not token:
    exit("Error: no token provided")

bot = Bot(token=token)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)


@dp.message_handler()
async def any_message(message: types.Message):
    pass


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
