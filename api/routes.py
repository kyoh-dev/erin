from logging import getLogger
from secrets import token_urlsafe

from passlib.context import CryptContext
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from starlette.responses import RedirectResponse

from core.constants import APP_PWD
from api.responses import upcoming_tasks_response, tasks_history_response, login_response
from core.sessions import put_session

logger = getLogger(__name__)
templates = Jinja2Templates(directory='templates')
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


async def home(request: Request) -> Jinja2Templates.TemplateResponse:
    return await upcoming_tasks_response(request)


async def history(request: Request) -> Jinja2Templates.TemplateResponse:
    return await tasks_history_response(request)


async def login(request: Request) -> Jinja2Templates.TemplateResponse:
    if request.method == 'GET':
        return await login_response(request)

    if request.method == 'POST':
        form_data = await request.form()
        input_pwd = form_data.get('password')

        if not pwd_context.verify(input_pwd, APP_PWD):
            return await login_response(request, "Invalid credentials, please try again.")

        session_key = token_urlsafe(32)
        put_session(session_key, request.client.host)
        request.session['key'] = session_key

        return RedirectResponse(url='/')
