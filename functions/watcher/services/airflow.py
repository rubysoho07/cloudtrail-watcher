import boto3

from services.common import *

airflow = boto3.client('mwaa')


def _set_mandatory_tag(event: dict):
    """ Set mandatory tag for MWAA(Managed Workflow for Apache Airflow) resources. """

    if 'Tags' in event['requestParameters'].keys():
        if check_contain_mandatory_tag_dict(event['requestParameters']['tags']) is True:
            return

    resource_arn = event['responseElements']['Arn']

    airflow.tag_resource(
        ResourceArn=resource_arn,
        Tags={
            'User': get_user_identity(event)
        }
    )


def _process_create_environment(event: dict, set_tag: bool = False) -> list:

    if set_tag is True:
        _set_mandatory_tag(event)

    return [event['requestParameters']['Name']]


def process_event(event: dict) -> dict:
    """ Process CloudTrail event for MWAA(Managed Workflow for Apache Airflow). """

    result = {
        "resource_id": None,
        "identity": get_user_identity(event),
        "region": event['awsRegion'],
        "source_ip_address": event['sourceIPAddress'],
        "event_name": event['eventName'],
        "event_source": get_service_name(event)
    }

    set_tag = check_set_mandatory_tag()

    if event['eventName'] == 'CreateEnvironment':
        result['resource_id'] = _process_create_environment(event, set_tag)
    else:
        message = f"Cannot process event: {event['eventName']}, eventID: f{event['eventID']}"
        result['error'] = message

    return result
