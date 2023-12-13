import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')

SQLITE_URL = os.getenv('SQLITE_URL')
NEW_SQLITE_URL = os.getenv('NEW_SQLITE_URL')

ID_ADMIN_1 = os.getenv('ID_ADMIN_1')
ID_ADMIN_2 = os.getenv('ID_ADMIN_2')
ID_ADMIN_3 = os.getenv('ID_ADMIN_3')

CERT_SHA256 = os.getenv('CERT_SHA256')
OUTLINE_API_URL = os.getenv('OUTLINE_API_URL')

