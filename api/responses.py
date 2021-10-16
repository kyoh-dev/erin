from logging import getLogger

from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from psycopg2 import DatabaseError

from core.constants import SESSIONS
from core.sessions import clear_expired_sessions
from db.tasks import get_upcoming_tasks, get_tasks_history

logger = getLogger(__name__)
templates = Jinja2Templates(directory='templates')


async def login_response(request: Request, exception: str = None):
    await request.send_push_promise('/static')
    return templates.TemplateResponse(
        'login.html', {'request': request, 'exception': exception}
    )


async def upcoming_tasks_response(request: Request):
    clear_expired_sessions()

    client_session_key = request.session.get('key')
    if not client_session_key:
        return RedirectResponse(url='/login')

    client_session_ip = request.client.host

    if (
            client_session_key in SESSIONS.keys()
            and client_session_ip == SESSIONS[client_session_key]['client_ip']
    ):
        tasks = get_upcoming_tasks()
        await request.send_push_promise('/static')
        return templates.TemplateResponse(
            'index.html', {'request': request, 'tasks': tasks}
        )
    else:
        return await login_response(request, "Session expired, please login to proceed.")


async def tasks_history_response(request: Request):
    clear_expired_sessions()

    client_session_key = request.session.get('key')
    if not client_session_key:
        return RedirectResponse(url='/login')

    client_session_ip = request.client.host

    if (
            client_session_key in SESSIONS.keys()
            and client_session_ip == SESSIONS[client_session_key]['client_ip']
    ):
        tasks = get_tasks_history()
        await request.send_push_promise('/static')
        return templates.TemplateResponse(
            'history.html', {'request': request, 'tasks': tasks}
        )
    else:
        return await login_response(request, "Session expired, please login to proceed.")
