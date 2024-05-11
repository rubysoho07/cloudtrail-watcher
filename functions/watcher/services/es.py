import boto3

from services.common import *

es = boto3.client('opensearch')


def _set_mandatory_tag(event: dict):
    """ Set mandatory tag for OpenSearch Domain resources. """

    if 'tagList' in event['requestParameters'].keys():
        if check_contain_mandatory_tag_list(event['requestParameters']['tagList']) is True:
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


def process_event(event: dict, set_tag: bool = False) -> dict:
    """ Process CloudTrail event for OpenSearch Service. """

    result = dict()

    if event['eventName'] == 'CreateDomain':
        result['resource_id'] = _process_create_domain(event, set_tag)
    else:
        message = f"Cannot process event: {event['eventName']}, eventID: f{event['eventID']}"
        result['error'] = message

    return result
