import boto3

from services.common import *

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


def process_event(event: dict) -> dict:
    """ Process CloudTrail event for RDS instances and clusters """

    if 'engine' in event['requestParameters'].keys() and event['requestParameters']['engine'] == 'docdb':
        event_source = 'documentdb'
    else:
        event_source = get_service_name(event)

    result = {
        "resource_id": None,
        "identity": get_user_identity(event),
        "region": event['awsRegion'],
        "source_ip_address": event['sourceIPAddress'],
        "event_name": event['eventName'],
        "event_source": event_source
    }

    if 'errorCode' in event.keys():
        result['error'] = f"{event['errorCode']}: check CloudTrail event - {event['eventID']}"
        return result

    set_tag = check_set_mandatory_tag()

    if event['eventName'] == "CreateDBCluster":
        result['resource_id'] = _process_create_db_cluster(event, set_tag)
    elif event['eventName'] == "CreateDBInstance":
        result['resource_id'] = _process_create_db_instance(event, set_tag)
    else:
        message = f"Cannot process event: {event['eventName']}, eventID: f{event['eventID']}"
        result['error'] = message

    return result
