import certifi
import ssl

import os

from dotenv import load_dotenv

sslcontext = ssl.create_default_context(cafile=certifi.where())

url = "https://swapi.dev/api/people/"

load_dotenv()

DB = os.getenv('PG_DB')
USER = os.getenv('PG_USER')
PASSWORD = os.getenv('PG_PASSWORD')
HOST = os.getenv('PG_HOST')
PORT = os.getenv('PG_PORT')

DNS = f"postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}"
