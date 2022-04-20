from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.dispatcher.flags.getter import get_flag
from aiogram.types import Message
from cachetools import TTLCache

from bot.const import THROTTLE_TIME_SPIN, THROTTLE_TIME_OTHER


class ThrottlingMiddleware(BaseMiddleware):
    caches = {
        "spin": TTLCache(maxsize=10_000, ttl=THROTTLE_TIME_SPIN),
        "default": TTLCache(maxsize=10_000, ttl=THROTTLE_TIME_OTHER)
    }

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any],
    ) -> Any:
        throttling_key = get_flag(data, "throttling_key")
        if throttling_key is not None and throttling_key in self.caches:
            if event.chat.id in self.caches[throttling_key]:
                return
            else:
                self.caches[throttling_key][event.chat.id] = None
        return await handler(event, data)
