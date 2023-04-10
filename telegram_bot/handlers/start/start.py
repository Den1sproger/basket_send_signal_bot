from aiogram import types
from ...bot_config import dp



WELCOME_TEXT = """
Привет👋👋👋
Я буду присылать тебе сигналы на ставку
в баскетбольных матчах🏀🏀🏀
"""


@dp.message_handler(commands=['start'])
async def start(message: types.Message) -> None:
    await message.answer(WELCOME_TEXT)