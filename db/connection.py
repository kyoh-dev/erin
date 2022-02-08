from logging import getLogger

from psycopg2.extensions import connection
from psycopg2 import connect, DatabaseError

from core.constants import DB_URI

logger = getLogger(__name__)


def get_connection() -> connection:
    try:
        conn = connect(DB_URI)
    except DatabaseError as ex:
        logger.exception("Database connection failed", ex)
    else:
        return conn
