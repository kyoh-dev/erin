from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles

from core.constants import APP_SECRET_KEY
from api.routes import home, add_task, complete_task, delete_task, history, login

routes = [
    Route('/', endpoint=home, methods=['GET', 'POST']),
    Route('/add-task', endpoint=add_task, methods=['POST']),
    Route('/complete-task', endpoint=complete_task, methods=['POST']),
    Route('/delete-task', endpoint=delete_task, methods=['POST']),
    Route('/history', endpoint=history),
    Route('/login', endpoint=login, methods=['GET', 'POST']),
    Mount('/static', StaticFiles(directory='static'), name='static'),
]

middleware = [
    #Middleware(HTTPSRedirectMiddleware),
    Middleware(
        SessionMiddleware, secret_key=APP_SECRET_KEY, max_age=600, https_only=True
    ),
]

app = Starlette(debug=True, routes=routes, middleware=middleware)
