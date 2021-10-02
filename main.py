from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles

from api.routes import home, history, login

routes = [
    Route('/', endpoint=home),
    Route('/history', endpoint=history),
    Route('/login', endpoint=login),
    Mount('/static', StaticFiles(directory='static'), name='static')
]

middleware = [
    Middleware(TrustedHostMiddleware, allowed_hosts=["*.kyoh.run", "erin.floral-wildflower-6316.fly.dev"]),
    Middleware(HTTPSRedirectMiddleware)
]

app = Starlette(debug=True, routes=routes)
