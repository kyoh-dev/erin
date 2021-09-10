from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

app = FastAPI(
    title='Erin',
    default_response_class=ORJSONResponse,
    docs_url="/api/docs", redoc_url=None
)

# app.include_router(api_router)
