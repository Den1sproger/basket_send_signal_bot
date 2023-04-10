import pymysql

from .db_config import *



class Database:
    """The class responsible for working with the database of subscribes"""

    def __init__(self):
        # Connect to the database
        # Подключение к базе данных
        self.connection = pymysql.connect(
            host=host, user=user, port=3306,
            password=password, database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )


    def get_mail_lists(self) -> list[str]:
        with self.connection:
            with self.connection.cursor() as cursor:
                insert_query = 'SELECT list_name FROM mail_lists'
                cursor.execute(insert_query)

                data = [row['list_name'] for row in cursor.fetchall()]
                
        return data
    

    def get_chat_id_by_subscribes(self, subscribes: list[str]) -> list[int]:
        with self.connection:
            with self.connection.cursor() as cursor:
                
                subscribes = f'{subscribes}'.replace('[', '(').replace(']', ')')
                insert_query = f'SELECT id FROM mail_lists WHERE list_name IN {subscribes}'
                cursor.execute(insert_query)
                lists_id = [row['id'] for row in cursor.fetchall()]

                lists_id = f'{lists_id}'.replace('[', '(').replace(']', ')')
                insert_query = f'SELECT user_id FROM bundle WHERE list_id IN {lists_id}'
                cursor.execute(insert_query)
                users_id = [row['user_id'] for row in cursor.fetchall()]

                users_id = f'{users_id}'.replace('[', '(').replace(']', ')')
                insert_query = f'SELECT chat_id FROM subscribers WHERE id IN {users_id}'
                cursor.execute(insert_query)

                data = [row['chat_id'] for row in cursor.fetchall()]

        return data