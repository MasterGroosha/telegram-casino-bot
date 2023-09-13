import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage

from bot.config_reader import Settings
from bot.fluent_loader import get_fluent_localization
from bot.handlers import default_commands, spin
from bot.middlewares.throttling import ThrottlingMiddleware
from bot.ui_commands import set_bot_commands


async def main():
    logging.basicConfig(level=logging.WARNING)
    config = Settings()

    bot = Bot(config.bot_token.get_secret_value(), parse_mode="HTML")

    # Выбираем нужный сторадж
    if config.fsm_mode == "redis":
        storage = RedisStorage.from_url(
            url=config.redis,
            connection_kwargs={"decode_responses": True}
        )
    else:
        storage = MemoryStorage()

    # Loading localization for bot
    l10n = get_fluent_localization(config.bot_language)

    # Создание диспетчера
    dp = Dispatcher(storage=storage, l10n=l10n, config=config)
    # Принудительно настраиваем фильтр на работу только в чатах один-на-один с ботом
    dp.message.filter(F.chat.type == "private")

    # Регистрация роутеров с хэндлерами
    dp.include_router(default_commands.router)
    dp.include_router(spin.router)

    # Регистрация мидлвари для троттлинга
    dp.message.middleware(ThrottlingMiddleware(config.throttle_time_spin, config.throttle_time_other))

    # Set bot commands in the UI
    await set_bot_commands(bot, l10n)

    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
