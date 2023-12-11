from aiogram.utils import executor
from outline_vpn.outline_vpn import OutlineVPN

from create_bot import dp
from database.database import create_db
from handlers import users_list
from config import CERT_SHA256, API_URL


async def on_startup(_):
    print('Добы день!')


# DB
create_db()
users_list.register_handlers_users(dp)

# client for OutlineApp
client = OutlineVPN(api_url=API_URL, cert_sha256=CERT_SHA256)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
