from datetime import datetime

from google.cloud import firestore
from google.cloud.firestore import Query

from core.utils import parse_date_string

db = firestore.AsyncClient()
current_date = datetime.today().strftime("%Y%m%d")


async def get_upcoming_tasks() -> list[dict[str, str]]:
    query = db.collection("tasks").where("due_date", ">=", current_date).stream()

    task_list = [task.to_dict() async for task in query]

    for task in task_list:
        task["due_date"] = parse_date_string(task["due_date"])

    return task_list


async def get_tasks_history() -> list[dict[str, str]]:
    query = (
        db.collection("tasks")
        .where("due_date", "<", current_date)
        .order_by("due_date", direction=Query.DESCENDING)
        .limit(25)
        .stream()
    )

    task_list = [task.to_dict() async for task in query]

    for task in task_list:
        task["due_date"] = parse_date_string(task["due_date"])

    return task_list
