from logging import getLogger
from datetime import datetime
from dataclasses import dataclass

from db.connection import get_connection

logger = getLogger(__name__)
today = datetime.today().strftime("%Y-%m-%d")


@dataclass
class NewTask:
    assignees: str
    description: str
    due_date: str


def get_upcoming_tasks() -> list[tuple]:
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                  id,
                  to_char(due_date::date, 'dd/mm'),
                  description,
                  assignees
                FROM public.task
                WHERE completed = false
                ORDER BY due_date, description;
            """
            )

            tasks = cursor.fetchall()

    return tasks


def get_tasks_history() -> list[tuple]:
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                  to_char(due_date::date, 'dd/mm/yy'),
                  description,
                  assignees
                FROM public.task
                WHERE completed = true
                ORDER BY due_date DESC, description;
            """
            )

            tasks = cursor.fetchall()

    return tasks


def add_task_record(task: NewTask) -> None:
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO public.task (assignees, description, due_date)
                VALUES (%s, %s, %s);
            """,
                (task.assignees, task.description, task.due_date),
            )


def complete_task_record(task_id: int) -> None:
    if task_id is None:
        raise TypeError("No task_id to complete.")

    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                UPDATE public.task
                SET completed = true
                WHERE id = %s;
            """,
                (task_id,),
            )


def delete_task_record(task_id: int) -> None:
    if task_id is None:
        raise TypeError("No task_id to delete.")

    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM public.task
                WHERE id = %s;
            """,
                (task_id,),
            )
