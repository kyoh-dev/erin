from logging import getLogger
from datetime import datetime, timedelta

from pytz import utc

from core.constants import SESSIONS

logger = getLogger(__name__)


def put_session(session_key: str, client_ip: str) -> None:
    SESSIONS[session_key] = {
        "client_ip": client_ip,
        "expires": datetime.now(utc) + timedelta(minutes=15),
    }


def clear_expired_sessions() -> None:
    for session in list(SESSIONS):
        if SESSIONS[session]['expires'] <= datetime.now(utc):
            del SESSIONS[session]
