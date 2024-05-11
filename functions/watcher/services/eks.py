import boto3

from services.common import *

eks = boto3.client('eks')


def _process_create_cluster(event: dict, set_tag: bool = False) -> list:
    """ Process ECS CreateCluster API. """

    if set_tag is True:
        if check_contain_mandatory_tag_dict(event['responseElements']['cluster']['tags']) is False:
            eks.tag_resource(
                resourceArn=event['responseElements']['cluster']['arn'],
                tags={'User': get_user_identity(event)}
            )

    return [event['responseElements']['cluster']['name']]


def process_event(event: dict, set_tag: bool = False) -> dict:
    """ Process CloudTrail event for ECS cluster """

    result = dict()

    if event['eventName'] == "CreateCluster":
        result['resource_id'] = _process_create_cluster(event, set_tag)
    else:
        message = f"Cannot process event: {event['eventName']}, eventID: f{event['eventID']}"
        result['error'] = message

    return result
