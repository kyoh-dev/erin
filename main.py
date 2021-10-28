from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.exceptions import HTTPException
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles

from core.constants import APP_SECRET_KEY
from api.exceptions import not_found, server_error
from api.routes import home, add_task, complete_task, delete_task, history, login, auth

routes = [
    Route('/', endpoint=home, methods=['GET', 'POST']),
    Route('/add-task', endpoint=add_task, methods=['POST']),
    Route('/completed', endpoint=complete_task, methods=['POST']),
    Route('/delete-task', endpoint=delete_task, methods=['POST']),
    Route('/history', endpoint=history),
    Route('/login', endpoint=login, methods=['GET']),
    Route('/auth', endpoint=auth, methods=['POST']),
    Mount('/static', StaticFiles(directory='static'), name='static'),
]

middleware = [
    Middleware(HTTPSRedirectMiddleware),
    Middleware(
        SessionMiddleware, secret_key=APP_SECRET_KEY, max_age=600, https_only=True
    ),
]

exception_handlers = {
    404: not_found,
    500: server_error,
    HTTPException: server_error,
}

app = Starlette(routes=routes, middleware=middleware, exception_handlers=exception_handlers)
