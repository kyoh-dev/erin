from starlette.requests import Request
from starlette.templating import Jinja2Templates
from starlette.authentication import SimpleUser

from core.constants import API_KEY
from api.utils import get_tasks

REQ_HEADERS = {
    "content-type": "application/json",
    "x-apikey": API_KEY,
    "cache-control": "no-cache",
}
templates = Jinja2Templates(directory='templates')


async def home(request: Request) -> Jinja2Templates.TemplateResponse:
    query = '/tasks?q={"due_date":{"$gte":{"$date":"$today"}}}'
    fields = '&h={"$fields": {"description": 1, "assignee": 1, "due_date": 1}}'

    response = get_tasks(query, fields, REQ_HEADERS)

    if isinstance(response, int):
        return templates.TemplateResponse(
            'error.html', {'request': request, 'error_code': response}
        )

    await request.send_push_promise('/static')
    return templates.TemplateResponse(
        'index.html', {'request': request, 'tasks': response}
    )


async def history(request: Request) -> Jinja2Templates.TemplateResponse:
    query = "/tasks"
    fields = '?h={"$fields": {"description": 1, "assignee": 1, "due_date": 1}}'

    response = get_tasks(query, fields, REQ_HEADERS)

    if isinstance(response, int):
        return templates.TemplateResponse(
            'error.html', {'request': request, 'error_code': response}
        )

    await request.send_push_promise('/static')
    return templates.TemplateResponse(
        'history.html', {'request': request, 'tasks': response}
    )
