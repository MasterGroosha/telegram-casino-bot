from asyncio import sleep
from textwrap import dedent

from aiogram import Router
from aiogram.dispatcher.filters import Command, Text
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message

from bot.const import START_POINTS, STICKER_FAIL, SPIN_TEXT, THROTTLE_TIME_SPIN
from bot.dice_check import get_combo_data
from bot.keyboards import get_spin_keyboard


async def cmd_spin(message: Message, state: FSMContext):
    user_data = await state.get_data()
    user_score = user_data.get("score", START_POINTS)

    if user_score == 0:
        await message.answer_sticker(sticker=STICKER_FAIL)
        await message.answer(
            "Ваш баланс равен нулю. Вы можете смириться с судьбой и продолжить жить своей жизнью, "
            "а можете нажать /start, чтобы начать всё заново. Или /stop, чтобы просто убрать клавиатуру."
        )
        return

    answer_text_template = """\
        Ваша комбинация: {combo_text} (№{dice_value}).
        {win_or_lose_text} Ваш счёт: <b>{new_score}</b>.
        """

    # Отправка дайса пользователю
    msg = await message.answer_dice(emoji="🎰", reply_markup=get_spin_keyboard())

    # Получение информации о дайсе
    score_change, combo_text = get_combo_data(msg.dice.value)
    if score_change < 0:
        win_or_lose_text = "К сожалению, вы не выиграли."
    else:
        win_or_lose_text = f"Вы выиграли {score_change} очков!"

    # Обновление счёта
    new_score = user_score + score_change
    await state.update_data(score=new_score)

    await sleep(THROTTLE_TIME_SPIN)
    await msg.reply(
        dedent(answer_text_template).format(
            combo_text=combo_text,
            dice_value=msg.dice.value,
            win_or_lose_text=win_or_lose_text,
            new_score=new_score
        )
    )


def register_spin_command(router: Router):
    flags = {"throttling_key": "spin"}
    router.message.register(cmd_spin, Command(commands="spin"), flags=flags)
    router.message.register(cmd_spin, Text(text=SPIN_TEXT), flags=flags)
