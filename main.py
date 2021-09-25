from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api.router import router as api_router

app = FastAPI(title="ErinBot", docs_url="/api/docs", redoc_url=None)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(api_router)
