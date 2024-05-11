import boto3

from services.common import *

kafka = boto3.client('kafka')


def _set_mandatory_tag(event: dict):
    """ Set mandatory tag for MSK resources. """

    if 'tags' in event['requestParameters'].keys():
        if check_contain_mandatory_tag_dict(event['requestParameters']['tags']) is True:
            return

    resource_arn = event['responseElements']['clusterArn']

    kafka.tag_resource(
        ResourceArn=resource_arn,
        Tags={
            'User': get_user_identity(event)
        }
    )


def _process_create_cluster_v2(event: dict, set_tag: bool = False) -> list:

    if set_tag is True:
        _set_mandatory_tag(event)

    return [event['responseElements']['clusterName']]


def process_event(event: dict, set_tag: bool = False) -> dict:
    """ Process CloudTrail event for MSK(Kafka). """

    result = dict()

    if event['eventName'] == 'CreateClusterV2':
        result['resource_id'] = _process_create_cluster_v2(event, set_tag)
    else:
        message = f"Cannot process event: {event['eventName']}, eventID: f{event['eventID']}"
        result['error'] = message

    return result
