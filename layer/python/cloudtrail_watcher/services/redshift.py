import boto3

from .common import *

redshift = boto3.client('redshift')
sts = boto3.client('sts')


def _get_redshift_cluster_arn(event: dict) -> str:
    """ Get ARN of Redshift cluster """

    account_id = event['userIdentity']['accountId']
    region = event['awsRegion']
    cluster_identifier = event['responseElements']['clusterIdentifier']

    return f"arn:aws:redshift:{region}:{account_id}:cluster:{cluster_identifier}"


def _process_create_cluster(event: dict, set_tag: bool = False) -> list:
    """ Process Redshift CreateCluster API """

    if set_tag is True:
        if 'tags' not in event['responseElements'].keys() or \
           check_contain_mandatory_tag_list(event['responseElements']['tags']) is False:
            redshift.create_tags(
                ResourceName=_get_redshift_cluster_arn(event),
                Tags=[{
                    'Key': 'User',
                    'Value': get_user_identity(event)
                }]
            )

    return [event['responseElements']['clusterIdentifier']]


def process_event(event: dict, set_tag: bool = False) -> dict:
    """ Process CloudTrail event for EC2 services """

    result = dict()

    if event['responseElements'] is None:
        result['error'] = f"response is None: check CloudTrail event - {event['eventID']}"
        return result

    if event['eventName'] == "CreateCluster":
        result['resource_id'] = _process_create_cluster(event, set_tag)
    else:
        message = f"Cannot process event: {event['eventName']}, eventID: f{event['eventID']}"
        result['error'] = message

    return result
