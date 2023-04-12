from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from ...bot_config import dp, bot, ADMIN
from .states import ProfileStatesGroup
from ...keyboards import get_mail_lists_kb
from database import Database



mail_lists = []
current_user_id: int


@dp.callback_query_handler(lambda callback: callback.data == 'add_mail_lists')
async def add_mail_list(callback: types.CallbackQuery) -> None:
    global current_user_id
    current_user_id = int(callback.message.text.split()[0])

    await ProfileStatesGroup.get_mail_lists_for_user.set()

    db = Database()

    await bot.send_message(
        chat_id=ADMIN,
        text='Выбирайте списки, если хотите закончить, жмите кнопку <b>cтоп</b>\n' \
            'Если вы ошиблись с выбором списков, то нажмите кнопку <b>заново</b>',
        reply_markup=get_mail_lists_kb(
            mail_lists=db.get_mail_lists(), stop='стоп'
        ),
        parse_mode='HTML'
    )
    await bot.delete_message(
        chat_id=ADMIN,
        message_id=callback.message.message_id
    )
    

@dp.message_handler(Text(equals='заново'), state=ProfileStatesGroup.get_mail_lists_for_user)
async def again(message: types.Message) -> None:
    global mail_lists
    mail_lists.clear()
    await message.answer('Выбирайте списки сначала')


@dp.message_handler(Text(equals='стоп'), state=ProfileStatesGroup.get_mail_lists_for_user)
async def stop_get_lists(message: types.Message, state=FSMContext) -> None:
    global mail_lists, current_user_id
    
    await state.finish()

    db = Database()

    for item in mail_lists:
        list_id = db.get_one_data_cell(
            query=f"SELECT id FROM mail_lists WHERE list_name = '{item}';",
            column='id'
        )
        db.action(
            f"INSERT INTO bundle VALUES ({current_user_id}, {list_id});"
        )

    await message.answer(
        "✅Пользователь успешно подписан на рассылку",
        reply_markup=types.ReplyKeyboardRemove()
    )
    current_user_id = 0
    mail_lists.clear()


@dp.message_handler(state=ProfileStatesGroup.get_mail_lists_for_user)
async def get_mail_list(message: types.Message) -> None:
    global mail_lists
    mail_lists.append(message.text)

    await message.answer(
        "Список добавлен\nЖмите на название списка рассылки или кнопку <b>стоп</b>",
        parse_mode='HTML'
    )


@dp.callback_query_handler(lambda callback: callback.data == 'unknown_user')
async def unknown_user(callback: types.CallbackQuery) -> None:
    global current_user_id
    current_user_id = 0

    await callback.answer("Пользователь игнорирован")
    await bot.delete_message(
        chat_id=ADMIN,
        message_id=callback.message.message_id
    )