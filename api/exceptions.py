from starlette.responses import Response
from starlette.requests import Request
from starlette.exceptions import HTTPException

from api.responses import templates


async def not_found(request: Request, exception: HTTPException) -> Response:
    return templates.TemplateResponse(
        'not_found.html', {'request': request, 'status_code': exception.status_code}
    )


async def server_error(request: Request, exception: HTTPException) -> Response:
    return templates.TemplateResponse(
        'error.html', {'request': request, 'status_code': exception.status_code}
    )
