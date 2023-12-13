from aiogram.utils import executor
from outline_vpn.outline_vpn import OutlineVPN

from create_bot import dp
from database.database import create_db
from handlers import handlers
from config import CERT_SHA256, OUTLINE_API_URL


async def on_startup(_):
    print('Добы день!')


# DB
create_db()
handlers.register_handlers_users(dp)

# client for OutlineApp
client = OutlineVPN(api_url=OUTLINE_API_URL, cert_sha256=CERT_SHA256)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
