from logging import getLogger
from datetime import datetime

from psycopg2 import DatabaseError

from db.connection import get_connection

logger = getLogger(__name__)
today = datetime.today().strftime('%Y-%m-%d')


def get_upcoming_tasks() -> list[tuple]:
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT
                  to_char(due_date::date, 'dd/mm/yyyy'),
                  description,
                  assignee
                FROM public.task
                WHERE due_date >= %s;
            """, (today,))

            tasks = cursor.fetchall()

    conn.close()
    return tasks


def get_tasks_history() -> list[tuple]:
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT
                  to_char(due_date::date, 'dd/mm/yyyy'),
                  description,
                  assignee
                FROM public.task
                WHERE due_date < %s;
            """, (today,))

            tasks = cursor.fetchall()

    conn.close()
    return tasks


def add_task(
    assignee: str, description: str, due_date: str
) -> None:
    ...
