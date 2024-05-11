import boto3

from services.common import *

dynamodb = boto3.client('dynamodb')


def _get_instance_resource_ids(event: dict) -> list:
    """ Get resource id from CloudTrail event. """
    result = []

    for instance in event['responseElements']['instancesSet']['items']:
        result.append(instance['instanceId'])

    return result


def _process_create_table(event: dict, set_tag: bool = False) -> list:

    resource_ids = [event['responseElements']['tableDescription']['tableName']]

    if set_tag is True:
        has_user_tags = False

        # Check tags
        if 'tags' in event['requestParameters'].keys():
            has_user_tags = check_contain_mandatory_tag_list(event['requestParameters']['tags'])

        # If mandatory tags are not set, set mandatory tags
        if has_user_tags is False:
            dynamodb.tag_resource(
                ResourceArn=event['responseElements']['tableDescription']['tableArn'],
                Tags=[{
                    'Key': 'User',
                    'Value': get_user_identity(event)
                }]
            )

    return resource_ids


def process_event(event: dict, set_tag: bool = False) -> dict:
    """ Process CloudTrail event for DynamoDB services """

    result = dict()

    if event['responseElements'] is None:
        result['error'] = f"response is null: eventName - {event['eventName']}, eventID: {event['eventID']},"
        return result

    if event['eventName'] == "CreateTable":
        result['resource_id'] = _process_create_table(event, set_tag)
    else:
        message = f"Cannot process event: {event['eventName']}, eventID: {event['eventID']}"
        result['error'] = message

    return result