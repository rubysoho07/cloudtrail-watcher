import boto3

from .common import *

rds = boto3.client('rds')


def _set_mandatory_tag(event: dict, set_tags: bool = False):
    """ Set mandatory tag for RDS cluster and instance. """
    if set_tags is False:
        return

    if check_contain_mandatory_tag_list(event['responseElements']['tagList']) is True:
        return

    if event['eventName'] == 'CreateDBCluster':
        resource_id = event['responseElements']['dBClusterArn']
    elif event['eventName'] == 'CreateDBInstance':
        resource_id = event['responseElements']['dBInstanceArn']
    else:
        raise ValueError(f"Cannot set mandatory tag for {event['eventName']}")

    rds.add_tags_to_resource(
        ResourceName=resource_id,
        Tags=[{
            'Key': 'User',
            'Value': get_user_identity(event)
        }]
    )


def _process_create_db_cluster(event: dict, set_tags: bool = False) -> list:
    """ Process CreateDBCluster event. """
    _set_mandatory_tag(event, set_tags)
    return [event['responseElements']['dBClusterIdentifier']]


def _process_create_db_instance(event: dict, set_tags: bool = False) -> list:
    """ Process CreateDBInstance event. """
    _set_mandatory_tag(event, set_tags)
    return [event['responseElements']['dBInstanceIdentifier']]


def process_event(event: dict, set_tag: bool = False) -> dict:
    """ Process CloudTrail event for RDS instances and clusters """

    result = dict()

    if 'engine' in event['requestParameters'].keys() and event['requestParameters']['engine'] == 'docdb':
        result['event_source'] = 'documentdb'
    else:
        result['event_source'] = get_service_name(event)

    if 'errorCode' in event.keys():
        result['error'] = f"{event['errorCode']}: check CloudTrail event - {event['eventID']}"
        return result

    if event['eventName'] == "CreateDBCluster":
        result['resource_id'] = _process_create_db_cluster(event, set_tag)
    elif event['eventName'] == "CreateDBInstance":
        result['resource_id'] = _process_create_db_instance(event, set_tag)
    else:
        message = f"Cannot process event: {event['eventName']}, eventID: f{event['eventID']}"
        result['error'] = message

    return result
