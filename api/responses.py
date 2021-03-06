from logging import getLogger

from starlette.requests import Request
from starlette.responses import Response, RedirectResponse
from starlette.templating import Jinja2Templates

from core.constants import SESSIONS
from core.sessions import clear_expired_sessions
from db.tasks import get_upcoming_tasks, get_tasks_history

logger = getLogger(__name__)
templates = Jinja2Templates(directory='templates')


async def login_response(request: Request, warning: str = None, error: str = None) -> Response:
    await request.send_push_promise('/static')
    return templates.TemplateResponse(
        'login.html', {'request': request, 'warning': warning, 'error': error}
    )


async def upcoming_tasks_response(request: Request) -> Response:
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
            'index.html', {'request': request, 'tasks': tasks, 'celebrate': False}
        )
    else:
        return await login_response(
            request, warning="Session expired, please login to continue."
        )


async def celebrate_response(request: Request) -> Response:
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
            'index.html', {'request': request, 'tasks': tasks, 'celebrate': True}
        )
    else:
        return await login_response(
            request, warning="Session expired, please login to continue."
        )


async def tasks_history_response(request: Request) -> Response:
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
        return await login_response(
            request, warning="Session expired, please login to continue."
        )
