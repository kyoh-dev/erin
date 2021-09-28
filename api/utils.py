from requests import get
from fastapi import Request
from fastapi.templating import Jinja2Templates

from core.constants import DB_BASE_URL

templates = Jinja2Templates(directory="templates")


def clean_date_string(date_string: str) -> str:
    return date_string.split("T", 1)[0]


def task_response_template(
    api_request: Request, query: str, fields: str, request_headers: dict, template: str
) -> templates.TemplateResponse:
    """
    Takes an API request for tasks with parameters and returns the template with the response data.

    :param api_request: The FastAPI Request object.
    :param query: Database API request query.
    :param fields: Database API field list.
    :param request_headers: Database API request headers.
    :param template: Jinja task template to return.
    :return: A FastAPI TemplateResponse with the requested Jinja template and response data.
    """
    response = get(url=f"{DB_BASE_URL}{query}{fields}", headers=request_headers)

    record_list = response.json()

    for record in record_list:
        record["due_date"] = clean_date_string(record["due_date"])

    if not response:
        return templates.TemplateResponse(
            "error.html", {"request": api_request, "error_code": response.status_code}
        )

    return templates.TemplateResponse(
        template, {"request": api_request, "tasks": record_list}
    )
