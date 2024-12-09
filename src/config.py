from dotenv import load_dotenv

import os


load_dotenv()

DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")

DB_CONNECTION = 'postgresql+asyncpg://sasha:NOV87CMvgEy7OKXP7kkOn0tgAUENFAeL@dpg-ctad51jtq21c73c3jvpg-a.oregon-postgres.render.com/lab3_au3f'
# DB_CONNECTION = os.environ.get("DB_CONNECTION")
