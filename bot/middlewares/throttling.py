from typing import Any, Awaitable, Callable, Dict, cast

from aiogram import BaseMiddleware
from aiogram.dispatcher.event.handler import HandlerObject
from aiogram.types import Update, Message
from cachetools import TTLCache

from bot.const import THROTTLE_TIME_SPIN, THROTTLE_TIME_OTHER


class ThrottlingMiddleware(BaseMiddleware):
    caches = {
        "spin": TTLCache(maxsize=10_000, ttl=THROTTLE_TIME_SPIN),
        "default": TTLCache(maxsize=10_000, ttl=THROTTLE_TIME_OTHER)
    }

    async def __call__(
            self,
            handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
            event: Update,
            data: Dict[str, Any],
    ) -> Any:
        real_handler: HandlerObject = data.get("handler")
        throttling_key = real_handler.flags.get("throttling_key")
        if throttling_key is not None and throttling_key in self.caches:
            event = cast(Message, event)  # Обещаем, что event будет иметь тип Message и только его
            if event.chat.id in self.caches[throttling_key]:
                return
            else:
                self.caches[throttling_key][event.chat.id] = None
        return await handler(event, data)
