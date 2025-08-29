import boto3

from .common import *

ecr = boto3.client('ecr')


def _process_create_repository(event: dict, set_tag: bool = False) -> list:
    """ Process ECR event for creating a repository. returns name of the repository. """

    repository_arn = event['responseElements']['repository']['repositoryArn']

    if set_tag is True:
        tags = ecr.list_tags_for_resource(resourceArn=repository_arn)

        exists_mandatory_tag = check_contain_mandatory_tag_list(tags['tags'])

        if exists_mandatory_tag is False:
            ecr.tag_resource(resourceArn=repository_arn,
                             tags=[{
                                 'Key': 'User',
                                 'Value': get_user_identity(event)
                             }])

    return [event['responseElements']['repository']['repositoryName']]


def process_event(event: dict, set_tag: bool = False) -> dict:
    """ Process CloudTrail event for CloudFront distribution. """

    result = dict()

    if event['eventName'] == "CreateRepository":
        result['resource_id'] = _process_create_repository(event, set_tag)
    else:
        message = f"Cannot process event: {event['eventName']}, eventID: {event['eventID']}"
        result['error'] = message

    return result
