import boto3

from botocore.exceptions import ClientError

from services.common import *

elasticache = boto3.client('elasticache')


def _set_mandatory_tag(event: dict):
    """ Set mandatory tag for ElastiCache resources. """
    try:
        if 'tags' in event['requestParameters'].keys():
            if check_contain_mandatory_tag(event['requestParameters']['tags']) is True:
                return

        resource_id = event['responseElements']['aRN']

        elasticache.add_tags_to_resource(
            ResourceName=resource_id,
            Tags=[{
                'Key': 'User',
                'Value': get_user_identity(event)
            }]
        )
    except ClientError as ce:
        print(ce.response)
        print(f"event ID: {event['eventID']}, event name: {event['eventName']}")


def _process_create_cache_cluster(event: dict, set_tag: bool = False) -> list:

    if set_tag is True:
        _set_mandatory_tag(event)

    return [event['responseElements']['aRN'].split(':')[-1]]


def _process_create_replication_group(event: dict, set_tag: bool = False) -> list:

    if set_tag is True:
        _set_mandatory_tag(event)

    return [event['responseElements']['aRN'].split(':')[-1]]


def process_event(event: dict) -> dict:
    """ Process CloudTrail event for ElastiCache. """

    result = {
        "resource_id": None,
        "identity": get_user_identity(event),
        "region": event['awsRegion'],
        "source_ip_address": event['sourceIPAddress'],
        "event_name": event['eventName'],
        "event_source": get_service_name(event)
    }

    set_tag = check_set_mandatory_tag()

    if event['eventName'] == 'CreateCacheCluster':
        result['resource_id'] = _process_create_cache_cluster(event, set_tag)
    elif event['eventName'] == 'CreateReplicationGroup':
        result['resource_id'] = _process_create_replication_group(event, set_tag)
    else:
        message = f"Cannot process event: {event['eventName']}, eventID: f{event['eventID']}"
        print(message)
        result['error'] = message

    return result
