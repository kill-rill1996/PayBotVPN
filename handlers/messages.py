from datetime import datetime

from database.tables import User
from handlers.service import is_debtor


def get_user_info_message(user: User, is_disabled: bool):
    text_message = f"Пользователь: {user.user_name} "

    if is_disabled:
        text_message += "❌\n"
    else:
        text_message += "✅\n"
    text_message += f'Баланс: {user.balance} ₽\n' \
                    + f'Дата истечения срока: {user.date_expiration.strftime("%d.%m.%Y")}\n'
    if is_debtor(user):
        days_of_delay = datetime.now().date() - user.date_expiration
        text_message += f'Количество дней просрочки: {days_of_delay.days} дней\n'
    text_message += f'*{user.description}'
    return text_message


def blocked_user_message(count: int):
    if count == 0:
        return 'Заблокированных пользователей нет'
    return f'Заблокированные пользователи ({count}):'
