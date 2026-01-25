import boto3

from .common import *

elasticache = boto3.client('elasticache')


def _set_mandatory_tag(event: dict):
    """ Set mandatory tag for ElastiCache resources. """

    if 'tags' in event['requestParameters'].keys():
        if check_contain_mandatory_tag_list(event['requestParameters']['tags']):
            return

    resource_id = event['responseElements']['aRN']

    elasticache.add_tags_to_resource(
        ResourceName=resource_id,
        Tags=[{
            'Key': 'User',
            'Value': get_user_identity(event)
        }]
    )


def _process_create_cache_cluster(event: dict, set_tag: bool = False) -> list:

    if set_tag:
        _set_mandatory_tag(event)

    return [event['responseElements']['aRN'].split(':')[-1]]


def _process_create_replication_group(event: dict, set_tag: bool = False) -> list:

    if set_tag:
        _set_mandatory_tag(event)

    return [event['responseElements']['aRN'].split(':')[-1]]


def process_event(event: dict, set_tag: bool = False) -> dict:
    """ Process CloudTrail event for ElastiCache. """

    result = dict()

    if event['eventName'] == 'CreateCacheCluster':
        result['resource_id'] = _process_create_cache_cluster(event, set_tag)
    elif event['eventName'] == 'CreateReplicationGroup':
        result['resource_id'] = _process_create_replication_group(event, set_tag)
    else:
        message = f"Cannot process event: {event['eventName']}, eventID: f{event['eventID']}"
        result['error'] = message

    return result
