import base64

from starlette.requests import Request
from starlette.authentication import requires
from starlette.templating import Jinja2Templates
from starlette.responses import PlainTextResponse, RedirectResponse

from core.constants import API_KEY
from api.utils import get_tasks

DB_REQ_HEADERS = {
    "content-type": "application/json",
    "x-apikey": API_KEY,
    "cache-control": "no-cache",
}
templates = Jinja2Templates(directory='templates')


@requires('authenticated', redirect='login')
async def home(request: Request) -> Jinja2Templates.TemplateResponse:
    query = '/tasks?q={"due_date":{"$gte":{"$date":"$today"}}}'
    fields = '&h={"$fields": {"description": 1, "assignee": 1, "due_date": 1}}'

    response = get_tasks(query, fields, DB_REQ_HEADERS)

    if isinstance(response, int):
        return templates.TemplateResponse(
            'error.html', {'request': request, 'error_code': response}
        )

    await request.send_push_promise('/static')
    return templates.TemplateResponse(
        'index.html', {'request': request, 'tasks': response}
    )


@requires('authenticated', redirect='login')
async def history(request: Request) -> Jinja2Templates.TemplateResponse:
    query = "/tasks"
    fields = '?h={"$fields": {"description": 1, "assignee": 1, "due_date": 1}}'

    response = get_tasks(query, fields, DB_REQ_HEADERS)

    if isinstance(response, int):
        return templates.TemplateResponse(
            'error.html', {'request': request, 'error_code': response}
        )

    await request.send_push_promise('/static')
    return templates.TemplateResponse(
        'history.html', {'request': request, 'tasks': response}
    )


async def login(request: Request) -> Jinja2Templates.TemplateResponse:
    await request.send_push_promise('/static')
    return templates.TemplateResponse(
        'login.html', {'request': request, 'exception': None}
    )


async def auth(request: Request):
    form_data = await request.form()

    user = 'default'
    password = form_data.get('password')
    auth_str = '%s:%s' % (user, password)
    b64_auth_str = base64.b64encode(auth_str.encode('utf-8'))

    return RedirectResponse(
        url='/',
        headers={
            'Authorization': 'Basic %s' % b64_auth_str
        }
    )
