import boto3

from .common import *

airflow = boto3.client('mwaa')


def _set_mandatory_tag(event: dict):
    """ Set mandatory tag for MWAA(Managed Workflow for Apache Airflow) resources. """

    if 'Tags' in event['requestParameters'].keys():
        if check_contain_mandatory_tag_dict(event['requestParameters']['tags']):
            return

    resource_arn = event['responseElements']['Arn']

    airflow.tag_resource(
        ResourceArn=resource_arn,
        Tags={
            'User': get_user_identity(event)
        }
    )


def _process_create_environment(event: dict, set_tag: bool = False) -> list:

    if set_tag:
        _set_mandatory_tag(event)

    return [event['requestParameters']['Name']]


def process_event(event: dict, set_tag: bool = False) -> dict:
    """ Process CloudTrail event for MWAA(Managed Workflow for Apache Airflow). """

    result = dict()

    if event['eventName'] == 'CreateEnvironment':
        result['resource_id'] = _process_create_environment(event, set_tag)
    else:
        message = f"Cannot process event: {event['eventName']}, eventID: f{event['eventID']}"
        result['error'] = message

    return result
