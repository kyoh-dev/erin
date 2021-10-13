from logging import getLogger
from datetime import datetime

from pytz import utc
from google.cloud import firestore
from google.cloud.exceptions import Conflict

logger = getLogger(__name__)
db_client = firestore.AsyncClient()


async def store_session(session_id: str, client_ip: str) -> tuple:
    result = None
    try:
        result = await db_client.collection("sessions").add(
            {
                "session_id": session_id,
                "client_ip": client_ip,
                "created_at": datetime.now(utc),
            }
        )
    except Conflict as error:
        logger.warning(
            f"Conflict raised when writing session: {session_id} for {client_ip}", error
        )

    return result


async def get_session(session_id: str, client_ip: str) -> dict[str, str]:
    query = (
        db_client.collection("sessions")
        .where("session_id", "==", session_id)
        .where("client_ip", "==", client_ip)
        .stream()
    )

    async for session in query:
        return session.to_dict()
