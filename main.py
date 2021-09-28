from typing import Callable, Union

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.staticfiles import StaticFiles

from api.router import router as api_router
from core.constants import ALLOWED_IP

app = FastAPI(title="ErinBot", docs_url="/api/docs", redoc_url=None)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*.kyoh.run", "erin.floral-wildflower-6316.fly.dev"],
)
app.add_middleware(HTTPSRedirectMiddleware)


@app.middleware("http")
async def validate_client_ip(
    api_request: Request, call_next: Callable
) -> Union[JSONResponse, Callable]:
    client_ip = str(api_request.client.host)

    if client_ip != ALLOWED_IP:
        response_data = {"response": f"HTTP {status.HTTP_401_UNAUTHORIZED}: Unauthorised IP address used."}
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED, content=response_data
        )

    return await call_next(api_request)


app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(api_router)
