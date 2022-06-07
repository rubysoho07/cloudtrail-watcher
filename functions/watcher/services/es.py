import boto3

from services.common import *

es = boto3.client('opensearch')


def _set_mandatory_tag(event: dict):
    """ Set mandatory tag for ElastiCache resources. """

    if 'tagList' in event['requestParameters'].keys():
        if check_contain_mandatory_tag_list(event['requestParameters']['tags']) is True:
            return

    resource_id = event['responseElements']['aRN']

    es.add_tags(
        ARN=resource_id,
        TagList=[{
            'Key': 'User',
            'Value': get_user_identity(event)
        }]
    )


def _process_create_domain(event: dict, set_tag: bool = False) -> list:
    """ Process CreateDomain event for OpenSearch Service. Returns domain name. """

    if set_tag is True:
        _set_mandatory_tag(event)

    return [event['responseElements']['domainStatus']['domainName']]


def process_event(event: dict) -> dict:
    """ Process CloudTrail event for OpenSearch Service. """

    result = {
        "resource_id": None,
        "identity": get_user_identity(event),
        "region": event['awsRegion'],
        "source_ip_address": event['sourceIPAddress'],
        "event_name": event['eventName'],
        "event_source": get_service_name(event)
    }

    set_tag = check_set_mandatory_tag()

    if event['eventName'] == 'CreateDomain':
        result['resource_id'] = _process_create_domain(event, set_tag)
    else:
        message = f"Cannot process event: {event['eventName']}, eventID: f{event['eventID']}"
        result['error'] = message

    return result
