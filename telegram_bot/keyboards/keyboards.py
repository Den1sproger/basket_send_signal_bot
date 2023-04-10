from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_mail_lists_kb(mail_lists: list[str],
                      stop: str = 'cancel') -> ReplyKeyboardMarkup:
    keyboard = [[KeyboardButton(list_)] for list_ in mail_lists]
    keyboard.append([KeyboardButton(stop)])
    keyboard.append([KeyboardButton('заново')])
    
    kb = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=keyboard
    )
    return kb