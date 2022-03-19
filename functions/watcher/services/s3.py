import boto3

from .common import *

s3 = boto3.resource('s3')


def _check_user_tag(tag_set: list) -> bool:
    """
        Check 'User' tag exists in S3 Bucket Tagging.
        Returns True when 'User' tag exists.
    """
    for tag in tag_set:
        if tag['Key'] == 'User':
            return True

    return False


def _process_create_bucket(event: dict, set_tags: bool = False) -> list:

    bucket_name = event['requestParameters']['bucketName']

    # Set mandatory tags
    if set_tags is True:
        bucket_tagging = s3.BucketTagging(bucket_name)
        tag_set = bucket_tagging.tag_set

        if _check_user_tag(tag_set) is False:
            tag_set.append({
                'Key': 'User',
                'Value': get_user_identity(event)
            })

            bucket_tagging.put(Tagging={
                'TagSet': tag_set
            })

    return [bucket_name]


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

    if event['eventName'] == "CreateBucket":
        result['resource_id'] = _process_create_bucket(event, set_tag)
    else:
        print(f"Cannot process event: {event['eventName']}, eventID: f{event['eventID']}")

    return result
