from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message

import logging

import config
import strings


logging.basicConfig(level=logging.INFO)

bot = Bot(config.TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())


@dp.message_handler(commands=("start_game", ))
async def start_game(message: Message):
    state = dp.current_state(user=message.from_user.id)


@dp.message_handler(commands=("start", ))
async def send_start_message(message: Message):
    start_mes = strings.START_MESSAGE + strings.HELP_MESSAGE
    await message.reply(start_mes)


@dp.message_handler(commands=("help", ))
async def send_help_message(message: Message):
    await message.reply(strings.HELP_MESSAGE)


@dp.message_handler()
async def reply_to_unknown_command(message: Message):
    await message.reply(strings.UNKNOWN_COMMAND)


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
