import boto3

from services.common import *


lambda_ = boto3.client('lambda')


def _process_create_function_20150331(event: dict, set_tags: bool = False) -> list:

    # Set mandatory tags
    if set_tags is True:
        function_arn = event['responseElements']['functionArn']
        function_tags = lambda_.list_tags(Resource=function_arn)

        if 'User' not in function_tags['Tags'].keys():
            lambda_.tag_resource(
                Resource=function_arn,
                Tags={
                    'User': get_user_identity(event)
                }
            )

    return [event['responseElements']['functionName']]


def process_event(event: dict) -> dict:
    """ Process CloudTrail event for Lambda functions """

    result = {
        "resource_id": None,
        "identity": get_user_identity(event),
        "region": event['awsRegion'],
        "source_ip_address": event['sourceIPAddress'],
        "event_name": event['eventName'],
        "event_source": get_service_name(event)
    }

    set_tag = check_set_mandatory_tag()

    if event['eventName'] == "CreateFunction20150331":
        result['resource_id'] = _process_create_function_20150331(event, set_tag)
    else:
        message = f"Cannot process event: {event['eventName']}, eventID: f{event['eventID']}"
        print(message)
        result['error'] = message

    return result
