from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles

from api.routes import home, history, login, auth
from api.auth import BasicAuthBackend, on_auth_error

routes = [
    Route('/', endpoint=home, methods=['GET', 'POST']),
    Route('/history', endpoint=history),
    Route('/login', endpoint=login),
    Route('/auth', endpoint=auth, methods=['POST']),
    Mount('/static', StaticFiles(directory='static'), name='static')
]

middleware = [
    #Middleware(TrustedHostMiddleware, allowed_hosts=["*.kyoh.run", "erin.floral-wildflower-6316.fly.dev"]),
    #Middleware(HTTPSRedirectMiddleware),
    Middleware(AuthenticationMiddleware, backend=BasicAuthBackend(), on_error=on_auth_error)
]

app = Starlette(debug=True, routes=routes, middleware=middleware)
