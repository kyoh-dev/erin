from typing import List, Dict, Union
from requests import get

from core.constants import DB_BASE_URL


def clean_date_string(date_string: str) -> str:
    return date_string.split("T", 1)[0]


def get_tasks(query: str, fields: str, request_headers: dict) -> Union[List[Dict[str, str]], int]:
    response = get(url=f"{DB_BASE_URL}{query}{fields}", headers=request_headers)
    if not response.ok:
        return response.status_code

    record_list = response.json()
    for record in record_list:
        record["due_date"] = clean_date_string(record["due_date"])

    return record_list
