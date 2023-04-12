from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


add_to_mail_ikb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                'Добавить в списки рассылки', callback_data='add_mail_lists'
            )
        ],
        [
            InlineKeyboardButton(
                'Неизвестный юзер', callback_data="unknown_user"
            )
        ]
    ]
)

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