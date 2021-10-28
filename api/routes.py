from typing import Union, Coroutine
from logging import getLogger
from secrets import token_urlsafe

from bleach import clean
from passlib.context import CryptContext
from psycopg2 import DatabaseError
from starlette.requests import Request
from starlette.responses import Response, RedirectResponse
from starlette.exceptions import HTTPException

from core.constants import APP_PWD
from core.sessions import create_session
from db.tasks import Task, add_task_record, complete_task_record, delete_task_record
from api.utils import collect_assignees
from api.responses import (
    upcoming_tasks_response,
    tasks_history_response,
    celebrate_response,
    login_response,
)

logger = getLogger(__name__)
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


async def home(request: Request) -> Response:
    return await upcoming_tasks_response(request)


async def add_task(request: Request) -> Union[Coroutine, Response]:
    form_data = await request.form()

    assignees = [
        form_data.get('assign-cara'),
        form_data.get('assign-connor'),
        form_data.get('assign-melanie'),
        form_data.get('assign-mitch')
    ]
    new_task = Task(
        assignees=collect_assignees(assignees),
        description=clean(form_data.get('task')),
        due_date=clean(form_data.get('due-date'))
    )

    try:
        add_task_record(new_task)
    except DatabaseError as ex:
        logger.exception(ex)
        raise HTTPException(status_code=500)

    return RedirectResponse(url='/')


async def complete_task(request: Request) -> Response:
    form_data = await request.form()
    task_id = form_data.get('complete-task-id')

    try:
        complete_task_record(task_id)
    except (TypeError, DatabaseError) as ex:
        logger.exception(ex)
        raise HTTPException(status_code=500)

    return await celebrate_response(request)


async def delete_task(request: Request) -> Union[Coroutine, Response]:
    form_data = await request.form()
    task_id = form_data.get('delete-task-id')

    try:
        delete_task_record(task_id)
    except (TypeError, DatabaseError) as ex:
        logger.exception(ex)
        raise HTTPException(status_code=500)

    return RedirectResponse(url='/')


async def history(request: Request) -> Response:
    return await tasks_history_response(request)


async def login(request: Request) -> Response:
    return await login_response(request)


async def auth(request: Request) -> Response:
    form_data = await request.form()
    input_pwd = clean(form_data.get('password'))

    if not pwd_context.verify(input_pwd, APP_PWD):
        return await login_response(
            request, error="Invalid credentials, please try again."
        )

    request.session['key'] = create_session(token_urlsafe(32), request.client.host)

    return RedirectResponse(url='/')
