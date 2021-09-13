from uuid import uuid4
from logging import getLogger

from boto3 import resource

logger = getLogger(__name__)


class Task:
    """
    Instantiates a task object to be read from and written to the database.
    """
