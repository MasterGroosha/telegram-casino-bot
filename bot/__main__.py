import asyncio
import logging

from aiogram import Bot, Dispatcher, Router
from aiogram.dispatcher.fsm.storage.memory import MemoryStorage
from aiogram.dispatcher.fsm.storage.redis import RedisStorage
from magic_filter import F

from bot.config_reader import Config, load_config
from bot.handlers.default_commands import register_default_commands
from bot.handlers.spin import register_spin_command
from bot.middlewares.throttling import ThrottlingMiddleware
from bot.ui_commands import set_bot_commands


async def main():
    logging.basicConfig(level=logging.WARNING)

    config: Config = load_config()
    bot = Bot(config.bot.token, parse_mode="HTML")

    default_router = Router()

    # Принудительно настраиваем фильтр на работу только в чатах один-на-один с ботом
    default_router.message.filter(F.chat.type == "private")

    # Регистрация хэндлеров
    register_default_commands(default_router)
    register_spin_command(default_router)

    # Создание диспетчера и навешивание роутера
    if config.bot.fsm_type == "redis":
        storage = RedisStorage.from_url(
            url=f"redis://default:{config.redis.password}@{config.redis.host}:{config.redis.port}",
            connection_kwargs={"decode_responses": True, "db": config.redis.db}
        )
        print("Set redis mode")
    else:
        storage = MemoryStorage()

    dp = Dispatcher(storage=storage)

    dp.include_router(default_router)

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
