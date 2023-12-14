import datetime
from typing import Dict
from dateutil.relativedelta import relativedelta
from . import tables
from .database import Session

from sqlalchemy import text


def add_to_db_users(data: Dict, transfer_date: str, key_id: str) -> None:
    with Session() as session:
        user = tables.User(
            user_name=data["user_name"],
            balance=data["balance"],
            date_expiration=data["date_expiration"],
            description=data["description"],
            key_id=key_id
        )
        session.add(user)
        session.commit()

        create_operation(user_id=user.id, summ=data['balance'], transfer_date=transfer_date)


def get_all_users_from_db():
    with Session() as session:
        users = session.query(tables.User).order_by(tables.User.user_name).all()
    return users


def get_user_from_db(user_name: str):
    with Session() as session:
        user = session.query(tables.User).filter_by(user_name=user_name).first()
    return user


def update_balance_and_date_for_user(user_name, balance):
    with Session() as session:
        user = session.query(tables.User).filter_by(user_name=user_name).first()
        user.balance += int(balance)
        if user.date_expiration < datetime.datetime.now().date():
            user.date_expiration = datetime.datetime.now().date() + relativedelta(months=int(balance)//100)
        else:
            user.date_expiration += relativedelta(months=int(balance)//100)
        session.commit()


def delete_user_from_db(user_name):
    with Session() as session:
        user = session.query(tables.User).filter_by(user_name=user_name).first()
        session.delete(user)
        session.query(tables.Operation).filter_by(user_id=user.id).delete()
        session.commit()
        return user


def create_operation(summ, transfer_date, user_id=None, user_name=None):
    with Session() as session:
        date_operation = datetime.datetime.strptime(transfer_date, "%d.%m.%Y").date()
        if user_id:
            operation = tables.Operation(user_id=user_id, date_operation=date_operation, summ=int(summ))
        elif user_name:
            id_user = session.query(tables.User).filter_by(user_name=user_name).first().id
            operation = tables.Operation(user_id=id_user, date_operation=date_operation, summ=int(summ))
        session.add(operation)
        session.commit()


def get_all_operations_from_db(limit=None):
    with Session() as session:
        if limit:
            query = text("SELECT * FROM operations LEFT JOIN users on operations.user_id = users.id ORDER BY date_operation DESC LIMIT 10")
            user_operations = session.execute(query)
            print(user_operations)
        else:
            user_operations = session.query(tables.Operation).all()
    return user_operations


def get_user_operations_from_db(user_id, limit=None):
    with Session() as session:
        if limit:
            user_operations = session.query(tables.Operation).filter_by(user_id=user_id).\
                order_by(tables.Operation.date_operation.desc()).limit(limit)
        else:
            user_operations = session.query(tables.Operation).filter_by(user_id=user_id).\
                order_by(tables.Operation.date_operation.desc()).limit(5)
    return user_operations


def block_user_db(key_id: str):
    with Session() as session:
        user = session.query(tables.User).filter_by(key_id=key_id).first()
        user.disabled = True
        session.commit()


def unblock_user_db(key_id: str):
    with Session() as session:
        user = session.query(tables.User).filter_by(key_id=key_id).first()
        user.disabled = False
        session.commit()


def get_blocked_user_from_db():
    with Session() as session:
        users = session.query(tables.User).filter_by(disabled=True).all()
    return users

