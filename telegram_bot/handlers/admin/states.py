from aiogram.dispatcher.filters.state import State, StatesGroup



class ProfileStatesGroup(StatesGroup):
    get_edit_message = State()
    get_mail_lists = State()
    get_mail_lists_for_user = State()