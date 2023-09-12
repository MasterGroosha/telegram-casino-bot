from asyncio import sleep

from aiogram import Router
from aiogram.enums.dice_emoji import DiceEmoji
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from bot.config_reader import Settings
from bot.const import THROTTLE_TIME_SPIN
from bot.dice_check import get_combo_text, get_score_change
from bot.filters import SpinTextFilter
from bot.keyboards import get_spin_keyboard

flags = {"throttling_key": "spin"}
router = Router()


@router.message(Command("spin"), flags=flags)
@router.message(SpinTextFilter(), flags=flags)
async def cmd_spin(message: Message, state: FSMContext, l10n: FluentLocalization, config: Settings):
    # Get current score
    user_data = await state.get_data()
    user_score = user_data.get("score", config.starting_points)

    if user_score == 0:
        # todo fix
        # await message.answer_sticker(sticker=STICKER_FAIL)
        await message.answer(l10n.format_value("zero-balance"))
        return

    # Отправка дайса пользователю
    msg = await message.answer_dice(emoji=DiceEmoji.SLOT_MACHINE, reply_markup=get_spin_keyboard(l10n))

    localized_combo_text = [
        l10n.format_value(item) for item in get_combo_text(msg.dice.value)
    ]

    score_change = get_score_change(msg.dice.value)

    if score_change < 0:
        win_or_lose_text = l10n.format_value("spin-fail")
    else:
        win_or_lose_text = l10n.format_value("spin-success", {"score_change": score_change})

    # Обновление счёта
    new_score = user_score + score_change
    await state.update_data(score=new_score)

    await sleep(THROTTLE_TIME_SPIN)
    await msg.reply(
        l10n.format_value(
            "after-spin",
            {
                "combo_text": ", ".join(localized_combo_text),
                "dice_value": msg.dice.value,
                "result_text": win_or_lose_text,
                "new_score": new_score
            }
        )
    )
