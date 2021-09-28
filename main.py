from fastapi import FastAPI
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.staticfiles import StaticFiles

from api.router import router as api_router

app = FastAPI(title="ErinBot", docs_url="/api/docs", redoc_url=None)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*.kyoh.run", "erin.floral-wildflower-6316.fly.dev"],
)
app.add_middleware(HTTPSRedirectMiddleware)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(api_router)
