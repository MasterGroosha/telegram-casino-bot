# Source: https://gist.github.com/MasterGroosha/963c0a82df348419788065ab229094ac

from typing import List, Tuple, Optional

#           0       1         2        3
casino = ["BAR", "виноград", "лимон", "семь"]


def is_winning_combo(combo) -> Tuple[bool, int]:
    """
    Проверка на выигрышную комбинацию

    :param combo: массив значений дайса (см. перем. casino)
    :return: пара "есть_выигрыш?", "изменение счёта игрока"
    """
    if combo[0] == "лимон" and combo[1] == "лимон":
        return True, 5
    elif combo[0] == "семь" and combo[1] == "семь" and combo[2] == "семь":
        return True, 10
    else:
        return False, -1


def convert_to_base4(number) -> int:
    """
    Преобразует число по основанию 10 в число по основанию 4

    :param number: Число по основанию 10
    :return: Число по основанию 4
    """
    result = []
    while number > 0:
        result.append(str(number % 4))
        number //= 4
    result.reverse()
    return int(''.join(result))


def get_casino_values(dice_value) -> Optional[List]:
    """
    Возвращает то, что было на конкретном дайсе-казино

    :param dice_value: Число, которое вернул Bot API
    :return: строку, содержащую все выпавшие элементы
    """
    try:
        number = convert_to_base4(dice_value) - 1
    except Exception as ex:
        print(f"Exception {type(ex)} with dice {dice_value}: {str(ex)}")
        return None

    str_number = str(number).zfill(3)  # Если длина строки меньше трёх, то добиваем спереди нулями
    result = []
    for letter in str_number:
        int_letter = int(letter)
        if int_letter > 3:
            int_letter = 3
        result.append(casino[int_letter % 4])
    result.reverse()
    return result
