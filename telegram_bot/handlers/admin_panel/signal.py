from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from ...bot_config import dp, bot, ADMIN
from database import Database
from ...keyboards import get_mail_lists_kb



edit_text = ''
mail_lists = []


class ProfileStatesGroup(StatesGroup):
    get_edit_message = State()
    get_mail_lists = State()


@dp.callback_query_handler(lambda callback: callback.data == 'edit_bet_signal')
async def edit_bet_signal(callback: types.CallbackQuery) -> None:
    await ProfileStatesGroup.get_edit_message.set()
    await bot.send_message(
        chat_id=ADMIN, text='Отправьте отредактированный текст'
    )


@dp.message_handler(state=ProfileStatesGroup.get_edit_message)
async def get_edit_message(message: types.Message) -> None:
    global edit_text
    edit_text = message.text

    db = Database()

    await ProfileStatesGroup.get_mail_lists.set()
    await message.answer(
        '✅Текст изменен✅\nВыбирайте списки, если хотите закончить, жмите кнопку <b>стоп</b>',
        parse_mode='HTML',
        reply_markup=get_mail_lists_kb(
            mail_lists=db.get_mail_lists(), stop='стоп'
        )
    )


@dp.message_handler(Text(equals='заново'), state=ProfileStatesGroup.get_mail_lists)
async def again(message: types.Message) -> None:
    global mail_lists
    mail_lists.clear()
    await message.answer('Выбирайте списки сначала')

    
@dp.message_handler(Text(equals='стоп'), state=ProfileStatesGroup.get_mail_lists)
async def mailing(message: types.Message, state=FSMContext) -> None:
    global edit_text, mail_lists

    if not mail_lists:
        await message.answer('Вы не выбрали ни одного списка, выберите хотя бы один')
    else:
        await state.finish()
        db = Database()
        users = db.get_chat_id_by_subscribes(mail_lists)

        for user in users:
            await bot.send_message(
                chat_id=user, text=edit_text
            )

        edit_text = ''
        mail_lists.clear()

        await message.answer(
            '✅Сигнал отправлен пользователям',
            reply_markup=types.ReplyKeyboardRemove()
        )


@dp.message_handler(state=ProfileStatesGroup.get_mail_lists)
async def add_mail_list(message: types.Message) -> None:
    global mail_lists
    mail_lists.append(message.text)

    await message.answer(
        "Список добавлен\nЖмите на название списка рассылки или кнопку <b>стоп</b>",
        parse_mode='HTML'
    )
    

@dp.callback_query_handler(lambda callback: callback.data == 'send_bet_signal')
async def send_bet_signal(callback: types.CallbackQuery) -> None:
    global edit_text
    edit_text = callback.message.text

    db = Database()

    await ProfileStatesGroup.get_mail_lists.set()
    await bot.send_message(
        chat_id=ADMIN,
        text='Выбирайте списки, если хотите закончить, жмите кнопку <b>стоп</b>',
        parse_mode='HTML',
        reply_markup=get_mail_lists_kb(
            mail_lists=db.get_mail_lists(), stop='стоп'
        )
    )