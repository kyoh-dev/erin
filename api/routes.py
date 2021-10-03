from passlib.context import CryptContext
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from starlette.responses import RedirectResponse

from core.constants import API_KEY, APP_PWD
from api.utils import get_tasks

DB_REQ_HEADERS = {
    "content-type": "application/json",
    "x-apikey": API_KEY,
    "cache-control": "no-cache",
}
templates = Jinja2Templates(directory='templates')
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


async def home(request: Request) -> Jinja2Templates.TemplateResponse:
    if request.session.get('authenticated'):
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

    return RedirectResponse(url='/login')


async def history(request: Request) -> Jinja2Templates.TemplateResponse:
    if request.session.get('authenticated'):
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

    return RedirectResponse(url='/login')


async def login(request: Request) -> Jinja2Templates.TemplateResponse:
    if request.method == 'GET':
        await request.send_push_promise('/static')
        return templates.TemplateResponse(
            'login.html', {'request': request, 'exception': None}
        )

    if request.method == 'POST':
        form_data = await request.form()
        input_pwd = form_data.get('password')
        if not pwd_context.verify(input_pwd, APP_PWD):
            return templates.TemplateResponse(
                    'login.html', {'request': request, 'exception': 'Invalid credentials, please try again.'}
                 )
        request.session['authenticated'] = True
        return RedirectResponse(url='/')
