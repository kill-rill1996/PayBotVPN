from datetime import datetime
import json

from database.database import Session
from database.tables import User, Operation
from database.database import create_db


def read_from_json_file():
    with open('users.json') as f:
        data = json.loads(f.read())
    return data


def convert_from_string_to_time(date_str: str):
    return datetime.strptime(date_str, "%d.%m.%Y").date()


def create_operation(user_id, operation_dict):
    with Session() as session:

        operation = Operation(
            user_id=user_id,
            date_operation=convert_from_string_to_time(operation_dict['date_operation']),
            summ=operation_dict['summ'])

        session.add(operation)
        session.commit()


def write_to_database():
    data_to_writing = read_from_json_file()

    with Session() as session:
        for name in data_to_writing.keys():
            user = User(
                user_name=name,
                balance=data_to_writing[name]['balance'],
                date_expiration=convert_from_string_to_time(data_to_writing[name]['date_expiration']),
                description=data_to_writing[name]['description'],
                key_id=data_to_writing[name]['key_id'],
                disabled=data_to_writing[name]['disabled'],
            )
            session.add(user)
            session.commit()

            for operation in data_to_writing[name]['operations']:
                create_operation(user.id, operation)


# НЕ ЗАБЫТЬ РАЗБЛОКИРОВАТЬ ПОЛЯ В ТАБЛИЦЕ
# print(read_from_json_file())
if __name__ == "__main__":
    create_db()
    write_to_database()
