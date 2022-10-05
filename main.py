from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message, CallbackQuery, \
        InlineKeyboardMarkup, InlineKeyboardButton, \
        ReplyKeyboardMarkup, KeyboardButton

import logging

import config
import guesser
import strings
from utils import UserStates

logging.basicConfig(level=logging.INFO)

bot = Bot(config.TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())


def get_reply_keyboard_markup(answers: tuple | list | str) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup()
    if isinstance(answers, str):
        keyboard.add(KeyboardButton(answers))
    else:
        for answer in answers:
            keyboard.add(KeyboardButton(answer))

    return keyboard


def get_inline_markup(buttons_info: dict) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)
    for name, data in buttons_info.items():
        markup.add(InlineKeyboardButton(text=name, callback_data=data))
    return markup


async def send_question(chat_id):
    state = dp.current_state(user=chat_id)
    data = await state.get_data()
    cur_tag = guesser.get_tag(data.get("tags", ""))
    question = guesser.get_question(cur_tag)
    await state.update_data(current_tag=cur_tag)
    answers = {"Да": "question_answer_yes", "Нет": "question_answer_no"}
    await bot.send_message(chat_id, question, reply_markup=get_inline_markup(answers))


@dp.message_handler(commands=("start_game", ), state="*")
async def start_game(message: Message):
    state = dp.current_state(user=message.from_user.id)
    if await state.get_state() == UserStates.GUESSING[0]:
        await state.reset_data()
    await state.set_state(UserStates.GUESSING[0])
    await send_question(message.from_id)


@dp.callback_query_handler(lambda c: "question_answer" in c.data, state=UserStates.GUESSING)
async def question_callback_handler(cb: CallbackQuery):
    state = dp.current_state(user=cb.from_user.id)
    data = await state.get_data()
    cur_tag = data.get("current_tag", "")
    tags = data.get("tags", [])
    bad_tags = data.get("bad_tags", [])

    if "yes" in cb.data:
        await state.update_data(tags=tags + [cur_tag])
    elif "no" in cb.data:
        await state.update_data(bad_tags=bad_tags + [cur_tag])

    await send_question(cb.from_user.id)


@dp.message_handler(commands=["tags"], state=UserStates.all())
async def send_tags(message: Message):
    state = dp.current_state(user=message.from_user.id)
    data = await state.get_data()
    st = await state.get_state()
    mes = f"{st}; {data}"
    await message.reply(mes)


@dp.message_handler(commands=("start", ))
async def send_start_message(message: Message):
    start_mes = strings.START_MESSAGE + strings.HELP_MESSAGE
    await message.reply(start_mes, reply_markup=get_reply_keyboard_markup(strings.COMMANDS))


@dp.message_handler(commands=("help", ))
async def send_help_message(message: Message):
    await message.reply(strings.HELP_MESSAGE, reply_markup=get_reply_keyboard_markup(strings.COMMANDS))


@dp.message_handler()
async def reply_to_unknown_command(message: Message):
    await message.reply(strings.UNKNOWN_COMMAND)


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
