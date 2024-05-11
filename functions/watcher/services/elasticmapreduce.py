import boto3

from services.common import *

emr = boto3.client('emr')


def _process_run_job_flow(event: dict, set_tag: bool = False) -> list:
    """ Process RunJobFlow event to create EMR cluster. """

    job_flow_id = event['responseElements']['jobFlowId']

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

    return [job_flow_id]


def process_event(event: dict, set_tag: bool = False) -> dict:
    """ Process CloudTrail event for EMR cluster """

    result = dict()

    if event['eventName'] == "RunJobFlow":
        result['resource_id'] = _process_run_job_flow(event, set_tag)
    else:
        message = f"Cannot process event: {event['eventName']}, eventID: f{event['eventID']}"
        result['error'] = message

    return result
