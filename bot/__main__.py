import asyncio

import structlog
from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
from structlog.typing import FilteringBoundLogger

from bot.config_reader import LogConfig, get_config, BotConfig, FSMMode, RedisConfig, GameConfig
from bot.fluent_loader import get_fluent_localization
from bot.handlers import default_commands, spin
from bot.logs import get_structlog_config
from bot.middlewares.throttling import ThrottlingMiddleware


async def main():
    log_config = get_config(model=LogConfig, root_key="logs")
    structlog.configure(**get_structlog_config(log_config))

    bot_config = get_config(model=BotConfig, root_key="bot")
    bot = Bot(
        token=bot_config.token.get_secret_value(),
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
        )
    )

    if bot_config.fsm_mode == FSMMode.REDIS:
        redis_config = get_config(model=RedisConfig, root_key="redis")
        storage = RedisStorage.from_url(
            url=str(redis_config.dsn),
            connection_kwargs={"decode_responses": True},
        )
    else:
        storage = MemoryStorage()

    # Loading localization for bot
    l10n = get_fluent_localization()

    game_config = get_config(model=GameConfig, root_key="game_config")

    # Creating dispatcher with some dependencies
    dp = Dispatcher(
        storage=storage,
        l10n=l10n,
        game_config=game_config,
    )
    # Make bot work only in PM (one-on-one chats) with bot
    dp.message.filter(F.chat.type == "private")

    # Register routers with handlers
    dp.include_router(default_commands.router)
    dp.include_router(spin.router)

    # Register throttling middleware
    dp.message.middleware(
        ThrottlingMiddleware(game_config.throttle_time_spin, game_config.throttle_time_other)
    )

    # Set bot commands in the UI
    # await set_bot_commands(bot, l10n)

    logger: FilteringBoundLogger = structlog.get_logger()
    await logger.ainfo("Starting polling...")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
