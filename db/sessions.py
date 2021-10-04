from datetime import datetime
from typing import Dict

from google.cloud import firestore

db = firestore.AsyncClient()


async def add_session_id(session_id: str) -> None:
    await db.collection("sessions").add({
        'session_id': session_id,
        'created_at': datetime.now()
    })


async def get_session_id(session_id: str) -> Dict[str, str]:
    query = db.collection("sessions") \
        .where("session_id", "==", session_id) \
        .stream()

    async for session in query:
        return session.to_dict()
