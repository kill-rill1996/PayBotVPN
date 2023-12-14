from datetime import datetime
from typing import List

from database.tables import User, Operation
from handlers.outline_services import get_user_transferred_data
from handlers.service import is_debtor


def get_user_info_message(user: User, is_disabled: bool):
    transferred_data = get_user_transferred_data(user.key_id)
    text_message = f"Пользователь: {user.user_name} ({transferred_data} GB)"

    if is_disabled:
        text_message += "❌\n"
    else:
        text_message += "✅\n"
    text_message += f'Дата истечения срока: {user.date_expiration.strftime("%d.%m.%Y")}\n'
    if is_debtor(user):
        days_of_delay = datetime.now().date() - user.date_expiration
        text_message += f'Количество дней просрочки: {days_of_delay.days} дней\n'
    text_message += f'*{user.description}'
    return text_message


def user_last_operations_message(user: User, operations: List[Operation]):
    message = f'Общая сумма {user.balance} р.\n'
    for operation in enumerate(operations):
        message = message + f'{operation[0] + 1}. Дата операции {operation[1].date_operation.strftime("%d.%m.%Y")}\n' \
                          f'Сумма {operation[1].summ}\n'
    return message


def blocked_user_message(count: int):
    if count == 0:
        return 'Заблокированных пользователей нет'
    return f'Заблокированные пользователи ({count}):'
