import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.dispatcher.fsm.storage.memory import MemoryStorage
from aiogram.dispatcher.fsm.storage.redis import RedisStorage
from magic_filter import F

from bot.config_reader import config
from bot.handlers import default_commands, spin
from bot.middlewares.throttling import ThrottlingMiddleware
from bot.ui_commands import set_bot_commands


async def main():
    logging.basicConfig(level=logging.WARNING)

    bot = Bot(config.bot_token.get_secret_value(), parse_mode="HTML")

    # Выбираем нужный сторадж
    if config.fsm_mode == "redis":
        storage = RedisStorage.from_url(
            url=config.redis,
            connection_kwargs={"decode_responses": True}
        )
    else:
        storage = MemoryStorage()

    # Создание диспетчера
    dp = Dispatcher(storage=storage)
    # Принудительно настраиваем фильтр на работу только в чатах один-на-один с ботом
    dp.message.filter(F.chat.type == "private")

    # Регистрация роутеров с хэндлерами
    dp.include_router(default_commands.router)
    dp.include_router(spin.router)

    # Регистрация мидлвари для троттлинга
    dp.message.middleware(ThrottlingMiddleware())

    # Установка команд в интерфейсе
    await set_bot_commands(bot)

    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
