from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from core.constants import API_KEY
from api.utils import task_response_template

REQ_HEADERS = {
    "content-type": "application/json",
    "x-apikey": API_KEY,
    "cache-control": "no-cache",
}

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def get_home(request: Request) -> Jinja2Templates.TemplateResponse:
    query = '/tasks?q={"due_date":{"$gte":{"$date":"$today"}}}'
    fields = '&h={"$fields": {"description": 1, "assignee": 1, "due_date": 1}}'
    page = task_response_template(
        request, query, fields, REQ_HEADERS, "index.html"
    )

    return page


@router.get("/history", response_class=HTMLResponse)
async def get_history(request: Request) -> Jinja2Templates.TemplateResponse:
    query = "/tasks"
    fields = '?h={"$fields": {"description": 1, "assignee": 1, "due_date": 1}}'
    page = task_response_template(
        request, query, fields, REQ_HEADERS, "history.html"
    )

    return page
