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
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
def get_upcoming_tasks(api_request: Request):
    query = '/tasks?q={"due_date":{"$gte":{"$date":"$today"}}}'
    fields = '&h={"$fields": {"description": 1, "assignee": 1, "due_date": 1}}'
    page = task_response_template(api_request, query, fields, REQ_HEADERS, 'index.html')

    return page


@router.get("/history", response_class=HTMLResponse)
def get_all_tasks(api_request: Request):
    query = "/tasks"
    fields = '&h={"$fields": {"description": 1, "assignee": 1, "due_date": 1}}'
    page = task_response_template(api_request, query, fields, REQ_HEADERS, 'history.html')

    return page
