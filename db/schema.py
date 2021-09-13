from logging import getLogger

from boto3 import resource

logger = getLogger(__name__)


def create_task_table(dynamodb: resource = None) -> dict:
    """
    Create the task table.
    :param dynamodb: DynamoDB connection resource.
    :return:
    """
    try:
        task_table = dynamodb.create_table(
            TableName='task',
            KeySchema=[
                {
                    'AttributeName': 'task_id',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'due_date',
                    'KeyType': 'RANGE'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'task_id',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'description',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'assignee',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'due_date',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'frequency',
                    'AttributeType': 'S'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 5
            }
        )
    except AttributeError as error:
        logger.info(error)
        raise
    else:
        return task_table
