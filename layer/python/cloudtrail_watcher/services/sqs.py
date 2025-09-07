import boto3

from .common import *

sqs = boto3.client('sqs')


def process_event(event: dict, set_tag: bool = False) -> dict:
    """ Process CloudTrail event for SQS """

    result = dict()

    if event['eventName'] == 'CreateQueue':
        result['resource_id'] = _process_create_queue(event, set_tag)
    else:
        message = f"Cannot process event: {event['eventName']}, eventID: {event['eventID']}"
        result['error'] = message

    return result


def _process_create_queue(event: dict, set_tag: bool = False) -> list:
    """ Process CreateQueue event """
    
    if set_tag is True:
        if 'tags' not in event['requestParameters'] or \
           check_contain_mandatory_tag_dict(event['requestParameters']['tags']) is False:
            sqs.tag_queue(
                QueueUrl=event['responseElements']['queueUrl'],
                Tags={
                    'User': get_user_identity(event)
                }
            )

    return [event['requestParameters']['queueName']]
