from textwrap import dedent

from aiogram import Router
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from bot.const import START_POINTS
from bot.keyboards import get_spin_keyboard


async def cmd_start(message: Message, state: FSMContext):
    start_text = """\
    <b>Добро пожаловать в наше виртуальное казино!</b>
    У вас {points} очков. Каждая попытка стоит 1 очко, а за выигрышные комбинации вы получите:
    
    3 одинаковых символа (кроме семёрки) — 7 очков
    7️⃣7️⃣▫️ — 5 очков (квадрат = что угодно)
    7️⃣7️⃣7️⃣ — 10 очков
    
    <b>Внимание</b>: бот предназначен исключительно для демонстрации, и ваши данные могут быть сброшены в любой момент! 
    Помните: лудомания — это болезнь, и никаких платных опций в боте нет.
    
    Убрать клавиатуру — /stop
    Показать клавиатуру, если пропала — /spin
    """
    await state.update_data(score=START_POINTS)
    await message.answer(dedent(start_text).format(points=START_POINTS), reply_markup=get_spin_keyboard())


async def cmd_stop(message: Message):
    await message.answer(
        "Клавиатура удалена. Начать заново: /start, вернуть клавиатуру и продолжить: /spin",
        reply_markup=ReplyKeyboardRemove()
    )


async def cmd_help(message: Message):
    help_text = \
        "В казино доступно 4 элемента: BAR, виноград, лимон и цифра семь. Комбинаций, соответственно, 64. " \
        "Для распознавания комбинации используется четверичная система, а пример кода " \
        "для получения комбинации по значению от Bot API можно увидеть " \
        "<a href='https://gist.github.com/MasterGroosha/963c0a82df348419788065ab229094ac'>здесь</a>.\n\n" \
        "Исходный код бота доступен на <a href='https://github.com/MasterGroosha/telegram-casino-bot'>GitHub</a> " \
        "и на <a href='https://git.groosha.space/shared/telegram-casino-bot'>GitLab</a>."
    await message.answer(help_text, disable_web_page_preview=True)


def register_default_commands(router: Router):
    flags = {"throttling_key": "default"}
    router.message.register(cmd_start, Command(commands="start"), flags=flags)
    router.message.register(cmd_stop, Command(commands="stop"), flags=flags)
    router.message.register(cmd_help, Command(commands="help"), flags=flags)
