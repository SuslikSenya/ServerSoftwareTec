from dotenv import load_dotenv

import os


load_dotenv()

DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")

# DB_CONNECTION = 'postgresql+asyncpg://sasha:Tsa0zS5iXO1Y6xyfvJXtDCVAcUuZAqQ6@dpg-cvdvtpnnoe9s73ejduvg-a.oregon-postgres.render.com/test_xaa1'
DB_CONNECTION = os.environ.get("DB_CONNECTION")
