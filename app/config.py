import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

YOOMONEY_WALLET_NUMBER = os.getenv("YOOMONEY_WALLET_NUMBER")
CLIENT_ID = os.getenv('CLIENT_ID')
REDIRECT_URI_BASE = os.getenv('REDIRECT_URI_BASE')

HOME_DB = os.getenv('HOME_DB', False)
LOCAL_DATABASE_URL = os.getenv('LOCAL_DATABASE_URL')
WORK_DATABASE_URL = os.getenv('WORK_DATABASE_URL')

DATABASE = "sqlite"  # or "postgres"