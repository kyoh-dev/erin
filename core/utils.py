from datetime import datetime
from requests import get
from typing import List, Dict, Union

from core.constants import DB_BASE_URL


def parse_date_string(date_string: str) -> str:
    return datetime.strptime(date_string, '%Y%m%d').strftime('%d/%m/%Y')


def get_tasks(query: str, fields: str, request_headers: dict) -> Union[List[Dict[str, str]], int]:
    response = get(url=f"{DB_BASE_URL}{query}{fields}", headers=request_headers)
    if not response.ok:
        return response.status_code

    record_list = response.json()
    for record in record_list:
        record["due_date"] = parse_date_string(record["due_date"])

    return record_list
