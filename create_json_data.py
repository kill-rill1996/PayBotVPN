from outline_vpn.outline_vpn import OutlineVPN
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from datetime import datetime
import json

from config import SQLITE_URL, API_URL, CERT_SHA256
from database import tables

engine = create_engine(f'{SQLITE_URL}', connect_args={"check_same_thread": False})
Session = sessionmaker(engine, autocommit=False, autoflush=False)

Base = declarative_base()


def read_all_users_from_db():
    users_dict = {}
    with Session() as session:
        users = session.query(tables.User).order_by(tables.User.user_name).all()
        for user in users:
            users_dict[f'{user.user_name}'] = {}
            users_dict[f'{user.user_name}']['balance'] = user.balance
            users_dict[f'{user.user_name}']['date_expiration'] = convert_date_to_str(user.date_expiration)
            users_dict[f'{user.user_name}']['description'] = user.description
            users_dict[f'{user.user_name}']['key_id'] = get_key_id(user.user_name)
            users_dict[f'{user.user_name}']['disabled'] = False
            users_dict[f'{user.user_name}']['operations'] = []

            operations = session.query(tables.Operation).filter_by(user_id=user.id)
            for operation in operations:
                users_dict[f'{user.user_name}']['operations'].append({
                    'summ': operation.summ,
                    'date_operation': convert_date_to_str(operation.date_operation),
                    'user_id': operation.user_id
                })

    write_data_in_json_file(users_dict)


def write_data_in_json_file(data: dict):
    with open("users.json", 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def convert_date_to_str(date: datetime):
    return datetime.strftime(date, "%d.%m.%Y")


def get_key_id(user_name: str):
    client = OutlineVPN(api_url=API_URL, cert_sha256=CERT_SHA256)
    for user_from_outline in client.get_keys():
        if user_name == user_from_outline.name:
            return user_from_outline.key_id
    print("Пользователь не найден")
    return -1

read_all_users_from_db()

