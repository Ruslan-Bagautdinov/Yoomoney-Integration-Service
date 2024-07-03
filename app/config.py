import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

RETURN_BASE = os.getenv('REDIRECT_URI_BASE')
RETURN_ENDPOINT = os.getenv('REDIRECT_ENDPOINT')
