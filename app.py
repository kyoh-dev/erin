from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import ORJSONResponse

app = FastAPI(
    title='Erin',
    default_response_class=ORJSONResponse,
    docs_url="/api/docs", redoc_url=None
)

app.mount('/static', StaticFiles(directory='static'), name='static')

# app.include_router(api_router)
