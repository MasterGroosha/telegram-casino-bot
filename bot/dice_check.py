# Source: https://gist.github.com/MasterGroosha/963c0a82df348419788065ab229094ac

from functools import lru_cache
from typing import List

from fluent.runtime import FluentLocalization


@lru_cache(maxsize=64)
def get_score_change(dice_value: int) -> int:
    """
    Проверка на выигрышную комбинацию

    :param dice_value: значение дайса (число)
    :return: изменение счёта игрока (число)
    """

    # Совпадающие значения (кроме 777)
    if dice_value in (1, 22, 43):
        return 7
    # Начинающиеся с двух семёрок (опять же, не учитываем 777)
    elif dice_value in (16, 32, 48):
        return 5
    # Джекпот (три семёрки)
    elif dice_value == 64:
        return 10
    else:
        return -1


def get_combo_parts(dice_value: int) -> List[str]:
    """
    Возвращает то, что было на конкретном дайсе-казино
    :param dice_value: значение дайса (число)
    :return: массив строк, содержащий все выпавшие элементы в виде текста

    Альтернативный вариант (ещё раз спасибо t.me/svinerus):
        return [casino[(dice_value - 1) // i % 4]for i in (1, 4, 16)]
    """
    # Do not edit these values; they are actually translation keys
    #           0       1         2        3
    values = ["bar", "grapes", "lemon", "seven"]

    dice_value -= 1
    result = []
    for _ in range(3):
        result.append(values[dice_value % 4])
        dice_value //= 4
    return result


@lru_cache(maxsize=64)
def get_combo_text(dice_value: int, l10n: FluentLocalization) -> str:
    parts: list[str] = get_combo_parts(dice_value)
    for i in range(len(parts)):
        parts[i] = l10n.format_value(parts[i])
    return ", ".join(parts)
