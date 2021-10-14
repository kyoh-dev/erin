from logging import getLogger
from datetime import datetime

from core.utils import date_display_fmt

logger = getLogger(__name__)
current_date = datetime.today().strftime("%Y%m%d")


def get_upcoming_tasks() -> list[dict[str, str]]:
    ...


def get_tasks_history() -> list[dict[str, str]]:
    ...


def add_task(
    assignee: str, description: str, due_date: str
) -> tuple:
    ...
