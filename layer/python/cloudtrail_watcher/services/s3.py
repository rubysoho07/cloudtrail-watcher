import boto3

from botocore.exceptions import ClientError

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
    if set_tags:
        bucket_tagging = s3.BucketTagging(bucket_name)

        try:
            tag_set = bucket_tagging.tag_set

            if not _check_user_tag(tag_set):
                tag_set.append({
                    'Key': 'User',
                    'Value': get_user_identity(event)
                })

                bucket_tagging.put(Tagging={
                    'TagSet': tag_set
                })
        except ClientError as ce:
            if ce.response['Error']['Code'] == 'NoSuchTagSet':
                bucket_tagging.put(Tagging={'TagSet': [{'Key': 'User', 'Value': get_user_identity(event)}]})
            else:
                raise ce

    return [bucket_name]


def process_event(event: dict, set_tag: bool = False) -> dict:
    """ Process CloudTrail event for Lambda functions """

    result = dict()

    if event['eventName'] == "CreateBucket":
        result['resource_id'] = _process_create_bucket(event, set_tag)
    else:
        message = f"Cannot process event: {event['eventName']}, eventID: f{event['eventID']}"
        result['error'] = message

    return result
