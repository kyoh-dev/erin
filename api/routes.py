from passlib.context import CryptContext
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from starlette.responses import RedirectResponse

from core.constants import APP_PWD
from db.crud import get_upcoming_tasks, get_tasks_history

templates = Jinja2Templates(directory='templates')
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


async def home(request: Request) -> Jinja2Templates.TemplateResponse:
    if request.session.get('authenticated'):
        tasks = await get_upcoming_tasks()

        await request.send_push_promise('/static')
        return templates.TemplateResponse(
            'index.html', {'request': request, 'tasks': tasks}
        )

    return RedirectResponse(url='/login')


async def history(request: Request) -> Jinja2Templates.TemplateResponse:
    if request.session.get('authenticated'):
        tasks = await get_tasks_history()

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
        request.session['authenticated'] = True
        return RedirectResponse(url='/')
