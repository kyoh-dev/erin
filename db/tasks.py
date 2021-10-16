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
                  to_char(due_date::date, 'dd/mm'),
                  description,
                  assignee
                FROM public.task
                WHERE due_date >= %s
                ORDER BY due_date DESC, description;
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
                WHERE due_date < %s
                ORDER BY due_date DESC, description;
            """, (today,))

            tasks = cursor.fetchall()

    conn.close()
    return tasks


def put_task(
    assignee: str, description: str, due_date: str
) -> None:
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO public.task (assignee, description, due_date)
                VALUES (%s, %s, %s)
            """, (assignee, description, due_date))

    conn.close()
