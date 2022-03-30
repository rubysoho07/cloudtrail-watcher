import boto3

from services.common import *

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


def process_event(event: dict) -> dict:
    """ Process CloudTrail event for ECS cluster """

    result = {
        "resource_id": None,
        "identity": get_user_identity(event),
        "region": event['awsRegion'],
        "source_ip_address": event['sourceIPAddress'],
        "event_name": event['eventName'],
        "event_source": get_service_name(event)
    }

    set_tag = check_set_mandatory_tag()

    if event['eventName'] == "CreateCluster":
        result['resource_id'] = _process_create_cluster(event, set_tag)
    else:
        message = f"Cannot process event: {event['eventName']}, eventID: f{event['eventID']}"
        result['error'] = message

    return result
