import boto3

from .common import *

sns = boto3.client('sns')

def process_event(event: dict, set_tag: bool = False) -> dict:
    """ Process CloudTrail event for sns """
	
    result = dict()

    if event['eventName'] == 'CreateTopic':
        result['resource_id'] = _process_create_topic(event, set_tag)
    else:
        message = f"Cannot process event: {event['eventName']}, eventID: {event['eventID']}"
        result['error'] = message

    return result


def _process_create_topic(event: dict, set_tag: bool = False) -> list:
    """ Process CreateTopic event """
    
    topic_arn = event['responseElements']['topicArn']
    topic_name = event['requestParameters']['name']
    
    if set_tag:
        if not check_contain_mandatory_tag_list(event['requestParameters']['tags']):
            sns.tag_resource(
                ResourceArn=topic_arn,
                Tags=[{'Key': 'User', 'Value': get_user_identity(event)}]
            )
    
    return [topic_name]