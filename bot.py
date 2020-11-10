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

SPIN_TEXT = "🎰 Испытать удачу!"


def get_spin_keyboard():
    # noinspection PyTypeChecker
    return types.ReplyKeyboardMarkup([[SPIN_TEXT]], resize_keyboard=True)


@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    start_text = "Добро пожаловать в наше виртуальное казино «Гудила Мороховая»!\n" \
                 "У вас 50 очков. Каждая попытка стоит 1 очко, а за выигрышные комбинации вы получите:\n\n" \
                 "🍋🍋▫️ — 5 очков\n" \
                 "7️⃣7️⃣7️⃣ — 10 очков\n\n" \
                 "<b>Внимание</b>: бот предназначен исключительно для демонстрации " \
                 "и ваши данные могут быть сброшены в любой момент! Лудомания — это болезнь, " \
                 "а никаких платных опций в боте нет."
    await message.answer(start_text, parse_mode="HTML", reply_markup=get_spin_keyboard())


@dp.message_handler()
async def any_message(message: types.Message):
    pass


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
