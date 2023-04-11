from aiogram import executor
from telegram_bot import dp
from telegram_bot.handlers.start.start import *
from telegram_bot.handlers.admin.signal import *


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)