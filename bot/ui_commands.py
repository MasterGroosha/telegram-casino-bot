from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats


async def set_bot_commands(bot: Bot):
    commands = [
            BotCommand(command="start", description="Перезапустить казино"),
            BotCommand(command="spin", description="Показать клавиатуру и сделать бросок"),
            BotCommand(command="stop", description="Убрать клавиатуру"),
            BotCommand(command="help", description="Справочная информация")
        ]
    await bot.set_my_commands(commands=commands, scope=BotCommandScopeAllPrivateChats())
