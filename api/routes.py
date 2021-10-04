from secrets import token_urlsafe, compare_digest

from passlib.context import CryptContext
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from starlette.responses import RedirectResponse

from core.constants import APP_PWD
from db.tasks import get_upcoming_tasks, get_tasks_history
from db.sessions import add_session_id, get_session_id

templates = Jinja2Templates(directory='templates')
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


async def home(request: Request) -> Jinja2Templates.TemplateResponse:
    request_id = request.session.get('id')
    server_id = await get_session_id(request_id)

    if compare_digest(request_id, server_id['session_id']):
        tasks = await get_upcoming_tasks()

        await request.send_push_promise('/static')
        return templates.TemplateResponse(
            'index.html', {'request': request, 'tasks': tasks}
        )

    return RedirectResponse(url='/login')


async def history(request: Request) -> Jinja2Templates.TemplateResponse:
    request_id = request.session.get('id')
    server_id = await get_session_id(request_id)

    if compare_digest(request_id, server_id['session_id']):
        tasks = await get_upcoming_tasks()

        await request.send_push_promise('/static')
        return templates.TemplateResponse(
            'history.html', {'request': request, 'tasks': tasks}
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

        session_id = token_urlsafe(32)
        request.session['id'] = session_id
        await add_session_id(session_id)

        return RedirectResponse(url='/')
