from typing import Union, Coroutine
from logging import getLogger
from time import sleep
from secrets import token_urlsafe

from bleach import clean
from passlib.context import CryptContext
from psycopg2 import DatabaseError
from starlette.requests import Request
from starlette.responses import Response
from starlette.responses import RedirectResponse

from core.constants import APP_PWD
from core.sessions import put_session
from db.tasks import add_task_record, complete_task_record, delete_task_record
from api.responses import (
    upcoming_tasks_response,
    tasks_history_response,
    login_response,
)

logger = getLogger(__name__)
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


async def home(request: Request) -> Response:
    return await upcoming_tasks_response(request)


async def add_task(request: Request) -> Union[Coroutine, Response]:
    form_data = await request.form()

    try:
        add_task_record(
            clean(form_data.get('assignee')),
            clean(form_data.get('task')),
            clean(form_data.get('due-date')),
        )
    except DatabaseError as ex:
        logger.exception(ex)
    finally:
        return RedirectResponse(url='/')


async def complete_task(request: Request):
    form_data = await request.form()
    task_id = form_data.get('complete-task-id')

    try:
        complete_task_record(task_id)
    except (TypeError, DatabaseError) as ex:
        logger.exception(ex)
    finally:
        # Leave time for the confetti to finish
        sleep(0.5)
        return RedirectResponse(url='/')


async def delete_task(request: Request) -> Union[Coroutine, Response]:
    form_data = await request.form()
    task_id = form_data.get('delete-task-id')

    try:
        delete_task_record(task_id)
    except (TypeError, DatabaseError) as ex:
        logger.exception(ex)
    finally:
        return RedirectResponse(url='/')


async def history(request: Request) -> Response:
    return await tasks_history_response(request)


async def login(request: Request) -> Response:
    if request.method == 'GET':
        return await login_response(request)

    if request.method == 'POST':
        form_data = await request.form()
        input_pwd = clean(form_data.get('password'))

        if not pwd_context.verify(input_pwd, APP_PWD):
            return await login_response(
                request, error="Invalid credentials, please try again."
            )

        session_key = token_urlsafe(32)
        put_session(session_key, request.client.host)
        request.session['key'] = session_key

        return RedirectResponse(url='/')
