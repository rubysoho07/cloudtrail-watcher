import boto3

from botocore.exceptions import ClientError

from services.common import *

emr = boto3.client('emr')


def _process_run_job_flow(event: dict, set_tag: bool = False) -> list:
    """ Process RunJobFlow event to create EMR cluster. """

    job_flow_id = event['responseElements']['jobFlowId']

    try:
        if set_tag is True:
            if 'tags' not in event['requestParameters'] or \
                    check_contain_mandatory_tag_list(event['requestParameters']['tags']) is False:
                emr.add_tags(
                    ResourceId=job_flow_id,
                    Tags=[{
                        'Key': 'User',
                        'Value': get_user_identity(event)
                    }]
                )

    except ClientError as ce:
        print(ce.response)
        print(f"event ID: {event['eventID']}, event name: {event['eventName']}")
    finally:
        return [job_flow_id]


def process_event(event: dict) -> dict:
    """ Process CloudTrail event for EMR cluster """

    result = {
        "resource_id": None,
        "identity": get_user_identity(event),
        "region": event['awsRegion'],
        "source_ip_address": event['sourceIPAddress'],
        "event_name": event['eventName'],
        "event_source": get_service_name(event)
    }

    set_tag = check_set_mandatory_tag()

    if event['eventName'] == "RunJobFlow":
        result['resource_id'] = _process_run_job_flow(event, set_tag)
    else:
        message = f"Cannot process event: {event['eventName']}, eventID: f{event['eventID']}"
        print(message)
        result['error'] = message

    return result
