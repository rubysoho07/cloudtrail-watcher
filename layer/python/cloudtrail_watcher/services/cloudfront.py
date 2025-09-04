import boto3

from .common import *

cloudfront = boto3.client('cloudfront')


def _process_create_distribution(event: dict, set_tag: bool = False) -> list:
    """ Process CloudTrail event for CloudFront distribution creation.
        Returns Distribution ID. """

    distribution_arn = event['responseElements']['distribution']['aRN']

    if set_tag is True:
        tags = cloudfront.list_tags_for_resource(Resource=distribution_arn)

        exists_mandatory_tag = check_contain_mandatory_tag_list(tags['Tags']['Items'])

        if exists_mandatory_tag is False:
            cloudfront.tag_resource(Resource=distribution_arn,
                                    Tags={'Items': [{
                                        'Key': 'User',
                                        'Value': get_user_identity(event)
                                    }]})

    return [event['responseElements']['distribution']['id']]


def process_event(event: dict, set_tag: bool = False) -> dict:
    """ Process CloudTrail event for CloudFront distribution. """

    result = dict()

    if event['eventName'] == "CreateDistribution":
        result['resource_id'] = _process_create_distribution(event, set_tag)
    else:
        message = f"Cannot process event: {event['eventName']}, eventID: {event['eventID']}"
        result['error'] = message

    return result
