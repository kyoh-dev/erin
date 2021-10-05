from datetime import datetime, timedelta
from typing import Dict

from google.cloud import firestore

db = firestore.AsyncClient()


async def store_session(session_id: str, client_ip: str) -> None:
    #TODO: Check document was actually stored in DB
    await db.collection("sessions").add({
        'session_id': session_id,
        'client_ip': client_ip,
        'created_at': datetime.now()
    })


async def get_session(session_id: str, client_ip: str):
    query = db.collection("sessions") \
        .where("session_id", "==", session_id) \
        .where("client_ip", "==", client_ip) \
        .stream()

    async for session in query:
        return session.to_dict()

