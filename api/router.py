from requests import request
from fastapi import APIRouter, HTTPException

from core.constants import DB_BASE_URL, API_KEY

REQ_HEADERS = {
    'content-type': 'application/json',
    'x-apkikey': API_KEY,
    'cache-control': 'no-cache'
}
router = APIRouter()


@router.get("/tasks/upcoming")
def get_upcoming_tasks():
    query = '/tasks?q={"due_date":{"$gte":{"$date":"$today"}}}'
    response = request('GET', f'{DB_BASE_URL}{query}', headers=REQ_HEADERS)
    return response.json()
