from asyncio import sleep
from contextlib import suppress

from aiogram import Router
from aiogram.enums.dice_emoji import DiceEmoji
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from bot.config_reader import Settings
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
        if config.send_gameover_sticker:
            # In case sticker file_id is invalid or missing
            with suppress(TelegramBadRequest):
                await message.answer_sticker(l10n.format_value("zero-balance-sticker"))
        await message.answer(l10n.format_value("zero-balance"))
        return

    # Send dice to user
    msg = await message.answer_dice(emoji=DiceEmoji.SLOT_MACHINE, reply_markup=get_spin_keyboard(l10n))

    # Check whether he won or not
    score_change = get_score_change(msg.dice.value)

    if score_change < 0:
        win_or_lose_text = l10n.format_value("spin-fail")
    else:
        win_or_lose_text = l10n.format_value("spin-success", {"score_change": score_change})

    # Updating score in FSM data
    new_score = user_score + score_change
    await state.update_data(score=new_score)

    # This delay is roughly equivalent of animation duration
    # of slot machine. Depending on dice value,
    # animation duration is different, but approx. 2 seconds
    await sleep(2.0)
    await msg.reply(
        l10n.format_value(
            "after-spin",
            {
                "combo_text": get_combo_text(msg.dice.value, l10n),
                "dice_value": msg.dice.value,
                "result_text": win_or_lose_text,
                "new_score": new_score
            }
        )
    )
