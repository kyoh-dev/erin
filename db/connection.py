from os import getenv
from logging import getLogger

from boto3 import resource

logger = getLogger(__name__)


def create_connection() -> resource:
    endpoint_url = getenv('ENDPOINT_URL')
    region_name = getenv('REGION_NAME')

    try:
        dynamodb = resource('dynamodb', endpoint_url=endpoint_url, region_name=region_name)
    except AttributeError as error:
        logger.info(error)
        raise
    else:
        return dynamodb
