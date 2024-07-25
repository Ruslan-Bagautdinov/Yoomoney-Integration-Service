import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

YM_REDIRECT_URI_BASE = os.getenv('YM_REDIRECT_URI_BASE')
YM_REDIRECT_ENDPOINT = os.getenv('YM_REDIRECT_ENDPOINT')
