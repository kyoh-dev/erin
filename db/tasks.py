from logging import getLogger
from datetime import datetime

from db.connection import get_connection

logger = getLogger(__name__)
today = datetime.today().strftime('%Y-%m-%d')


def get_upcoming_tasks() -> list[tuple]:
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT
                  id,
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
                  to_char(due_date::date, 'dd/mm/yy'),
                  description,
                  assignee
                FROM public.task
                WHERE due_date < %s
                ORDER BY due_date DESC, description;
            """, (today,))

            tasks = cursor.fetchall()

    conn.close()
    return tasks


def add_task_record(
    assignee: str, description: str, due_date: str
) -> None:
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO public.task (assignee, description, due_date)
                VALUES (%s, %s, %s)
            """, (assignee, description, due_date))

            conn.commit()

    conn.close()


def delete_task_record(task_id: int) -> None:
    if task_id is None:
        raise TypeError('No task_id to delete.')

    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                DELETE FROM public.task
                WHERE id = %s
            """, (task_id,))

            conn.commit()

    conn.close()
