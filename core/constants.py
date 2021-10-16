from os import environ

APP_PWD = environ['APP_PWD']
APP_SECRET_KEY = environ['APP_SECRET_KEY']

DB_NAME = environ['DB_NAME']
DB_PASSWORD = environ['DB_PASSWORD']
DB_SERVER = environ['DB_SERVER']
DB_URI = f"postgres://{DB_NAME}:{DB_PASSWORD}@{DB_SERVER}/{DB_NAME}"

SESSIONS = {}
