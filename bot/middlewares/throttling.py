from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.dispatcher.event.handler import HandlerObject
from aiogram.types import Update
from cachetools import TTLCache

from bot.const import THROTTLE_TIME_SPIN, THROTTLE_TIME_OTHER

caches = {
    "spin": TTLCache(maxsize=10_000, ttl=THROTTLE_TIME_SPIN),
    "default": TTLCache(maxsize=10_000, ttl=THROTTLE_TIME_OTHER)
}


class ThrottlingMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
            event: Update,
            data: Dict[str, Any],
    ) -> Any:
        real_handler: HandlerObject = data.get("handler")
        throttling_key = real_handler.flags.get("throttling_key")
        if throttling_key is not None and throttling_key in caches:
            # Поскольку мидлварь только для Message, то тип Update всегда Message.
            # И проверку if isinstance(event, Message) можно пропустить, хотя PyCharm будет ругаться
            if event.chat.id in caches[throttling_key]:
                return
            else:
                caches[throttling_key][event.chat.id] = None
        return await handler(event, data)
