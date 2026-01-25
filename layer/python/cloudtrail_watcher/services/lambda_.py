import boto3

from .common import *


lambda_ = boto3.client('lambda')


def _process_create_function_20150331(event: dict, set_tags: bool = False) -> list:

    # Set mandatory tags
    if set_tags:
        function_arn = event['responseElements']['functionArn']
        function_tags = lambda_.list_tags(Resource=function_arn)

        tags_list = function_tags['Tags'].keys()

        if 'User' not in tags_list:
            lambda_.tag_resource(
                Resource=function_arn,
                Tags={
                    'User': get_user_identity(event)
                }
            )

    return [event['responseElements']['functionName']]


def process_event(event: dict, set_tag: bool = False) -> dict:
    """ Process CloudTrail event for Lambda functions """

    result = dict()

    if event['eventName'] == "CreateFunction20150331":
        result['resource_id'] = _process_create_function_20150331(event, set_tag)
    else:
        message = f"Cannot process event: {event['eventName']}, eventID: f{event['eventID']}"
        result['error'] = message

    return result
