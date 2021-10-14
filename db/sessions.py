from logging import getLogger
from datetime import datetime

from pytz import utc

logger = getLogger(__name__)


def store_session(session_id: str, client_ip: str) -> tuple:
    ...


def get_session(session_id: str, client_ip: str) -> dict[str, str]:
    ...
