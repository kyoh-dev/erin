import base64
import binascii

from starlette.requests import Request
from starlette.authentication import AuthenticationError, AuthenticationBackend, AuthCredentials, SimpleUser
from starlette.templating import Jinja2Templates
from passlib.context import CryptContext

from api.routes import templates
from core.constants import APP_PWD

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class BasicAuthBackend(AuthenticationBackend):
    async def authenticate(self, request):
        if "Authorization" not in request.headers:
            return

        auth = request.headers["Authorization"]
        try:
            scheme, credentials = auth.split()
            if scheme.lower() != 'basic':
                return
            decoded = base64.b64decode(credentials).decode("ascii")
        except (ValueError, UnicodeDecodeError, binascii.Error) as exc:
            raise AuthenticationError('Value decoding error.')

        username, _, password = decoded.partition(":")
        if not verify_password(password):
            raise AuthenticationError('Invalid credentials.')

        return AuthCredentials(["authenticated"]), SimpleUser(username)


def verify_password(input_pwd: str, hashed_pwd: str = APP_PWD) -> bool:
    return pwd_context.verify(input_pwd, hashed_pwd)


def on_auth_error(request: Request, exception: Exception) -> Jinja2Templates.TemplateResponse:
    return templates.TemplateResponse(
        'login.html', {'request': request, 'exception': exception}
    )
