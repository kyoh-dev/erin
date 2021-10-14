from psycopg2 import connect

from core.constants import DB_URI


def get_connection():
    return connect(DB_URI)
