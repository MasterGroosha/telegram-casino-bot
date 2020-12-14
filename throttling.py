from math import inf
from aiogram import types
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from cachetools import TTLCache
from const import THROTTLE_TIME_OTHER, THROTTLE_TIME_SPIN

# Разные по продолжительности кэши для разных типов действий (запуск игрового автомата или /-команды)
caches = {
    "default": TTLCache(maxsize=inf, ttl=THROTTLE_TIME_OTHER),
    "spin": TTLCache(maxsize=inf, ttl=THROTTLE_TIME_SPIN)
}


def rate_limit(key="default"):
    """
    Декоратор для нанесения троттлинга на хэндлер

    :param key: идентификатор конкретного троттлинга
    """

    def decorator(func):
        setattr(func, 'throttling_key', key)
        return func
    return decorator


class ThrottlingMiddleware(BaseMiddleware):
    """
    Миддлварь для "умного" троттлинга
    """

    def __init__(self):
        super(ThrottlingMiddleware, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        """
        Этот хэндлер сработает при обработке сообщения (класс Message)

        :param message: входящее сообщение в Telegram
        """
        # Получаем текущий хэндлер
        handler = current_handler.get()

        # Определяем, какой кэш надо использовать
        throttling_key = getattr(handler, 'throttling_key', None)

        # Если такой кэш есть в наличии, то либо добавляем chat_id
        # во временный список и выполняем хэндлер, либо пропускаем вообще
        # Chat_ID можно использовать, т.к. бот не должен работать в группах
        if throttling_key and throttling_key in caches:
            if not caches[throttling_key].get(message.chat.id):
                caches[throttling_key][message.chat.id] = True
                return
            else:
                raise CancelHandler
