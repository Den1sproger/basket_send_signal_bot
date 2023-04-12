from aiogram import types
from ...bot_config import dp, bot, ADMIN
from ...keyboards import add_to_mail_ikb
from database import Database



@dp.message_handler(lambda message: message.text == '+')
async def add_user(message: types.Message) -> None:
    chat_id = message.from_user.id
    if chat_id != ADMIN:
        username = message.from_user.username
        if not username:
            username = message.from_user.full_name

        query = f"INSERT INTO subscribers (nickname, chat_id) VALUES ('{username}', {chat_id});"

        db = Database()
        db.action(query)
        
        user_id = db.get_one_data_cell(
            query="SELECT MAX(id) FROM subscribers;",
            column="MAX(id)"
        )

        await bot.send_message(
            chat_id=ADMIN,
            text=f'{user_id} @{username} подана заявка на подписку',
            reply_markup=add_to_mail_ikb
        )