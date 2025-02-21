from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from fluent.runtime import FluentLocalization

from bot.config_reader import Settings
from bot.keyboards import get_spin_keyboard

flags = {"throttling_key": "default"}
router = Router()


@router.message(Command("start"), flags=flags)
async def cmd_start(message: Message, state: FSMContext, l10n: FluentLocalization, config: Settings):
    start_text = l10n.format_value("start-text", {"points": config.starting_points})

    await state.update_data(score=config.starting_points)
    await message.answer(start_text, reply_markup=get_spin_keyboard(l10n))


@router.message(Command("stop"), flags=flags)
async def cmd_stop(message: Message, l10n: FluentLocalization):
    await message.answer(
        l10n.format_value("stop-text"),
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(Command("help"), flags=flags)
async def cmd_help(message: Message, l10n: FluentLocalization):
    await message.answer(
        l10n.format_value("help-text"),
        disable_web_page_preview=True
    )
