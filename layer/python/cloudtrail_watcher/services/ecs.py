import boto3

from .common import *

ecs = boto3.client('ecs')


def _process_create_cluster(event: dict, set_tag: bool = False) -> list:
    """ Process ECS CreateCluster API. """

    if set_tag is True:
        if check_contain_mandatory_tag_list(event['responseElements']['cluster']['tags']) is False:
            ecs.tag_resource(
                resourceArn=event['responseElements']['cluster']['clusterArn'],
                tags=[{
                    'key': 'User',
                    'value': get_user_identity(event)
                }]
            )

    return [event['responseElements']['cluster']['clusterName']]


def process_event(event: dict, set_tag: bool = False) -> dict:
    """ Process CloudTrail event for ECS cluster """

    result = dict()

    if event['eventName'] == "CreateCluster":
        result['resource_id'] = _process_create_cluster(event, set_tag)
    else:
        message = f"Cannot process event: {event['eventName']}, eventID: f{event['eventID']}"
        result['error'] = message

    return result
