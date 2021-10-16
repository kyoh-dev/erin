from logging import getLogger
from secrets import token_urlsafe

from bleach import clean
from passlib.context import CryptContext
from psycopg2 import DatabaseError
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from starlette.responses import RedirectResponse

from core.constants import APP_PWD
from core.sessions import put_session
from db.tasks import put_task
from api.responses import upcoming_tasks_response, tasks_history_response, login_response, add_task_error_response

logger = getLogger(__name__)
templates = Jinja2Templates(directory='templates')
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


async def home(request: Request) -> Jinja2Templates.TemplateResponse:
    return await upcoming_tasks_response(request)


async def add_task(request: Request):
    form_data = await request.form()

    try:
        put_task(
            clean(form_data.get('assignee')),
            clean(form_data.get('task')),
            clean(form_data.get('due-date'))
        )
    except DatabaseError as ex:
        logger.exception(ex)
        return add_task_error_response(request, 'There was a problem adding that task, please try again.')
    else:
        return RedirectResponse('/')


async def history(request: Request) -> Jinja2Templates.TemplateResponse:
    return await tasks_history_response(request)


async def login(request: Request) -> Jinja2Templates.TemplateResponse:
    if request.method == 'GET':
        return await login_response(request)

    if request.method == 'POST':
        form_data = await request.form()
        input_pwd = clean(form_data.get('password'))

        if not pwd_context.verify(input_pwd, APP_PWD):
            return await login_response(request, error="Invalid credentials, please try again.")

        session_key = token_urlsafe(32)
        put_session(session_key, request.client.host)
        request.session['key'] = session_key

        return RedirectResponse(url='/')
