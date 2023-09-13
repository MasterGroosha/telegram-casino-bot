from functools import cache

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from fluent.runtime import FluentLocalization


@cache
def get_spin_keyboard(l10n: FluentLocalization):
    keyboard = [
        [KeyboardButton(text=l10n.format_value("spin-button-text"))]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
