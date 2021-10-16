from logging import getLogger

from psycopg2 import connect, Error

from core.constants import DB_URI

logger = getLogger(__name__)


def get_connection():
    try:
        conn = connect(DB_URI)
    except Error as ex:
        logger.exception('Database connection failed.', ex)
    else:
        return conn
