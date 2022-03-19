import os
import gzip
import json
import importlib
import traceback

import boto3

from .services import common


s3 = boto3.client('s3')
sns = boto3.resource('sns')


def process_event_by_service(record: dict) -> dict:
    """ Process event by service name"""

    service_name = common.get_service_name(record)
    module = importlib.import_module(f"services.{service_name}")

    return module.process_event(record)


def notify(summary: dict):
    """ Send notification to SNS topic """
    if 'SNS_TOPIC_ARN' not in os.environ.keys():
        raise ValueError('SNS Topic not found')

    topic = sns.Topic(os.environ['SNS_TOPIC_ARN'])
    response = topic.publish(Message=json.dumps(summary))

    return response


def handler(event, context):
    print(event)

    # Get object information
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    # Transform raw data to dict type
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        data = json.load(gzip.GzipFile(fileobj=response['Body']))

        # Check each event
        for record in data['Records']:
            if record['readOnly'] is False:
                continue

            # Process event
            result = process_event_by_service(record)

            # Add account ID information
            if 'recipientAccountId' in event.keys():
                result['account_id'] = event['recipientAccountId']
            else:
                result['account_id'] = None

            # Send notification to SNS topic
            response = notify(result)

            return {
                'message': result,
                'message_id': response['MessageId'],
                'sequence_number': response['SequenceNumber']
            }
    except Exception as e:
        traceback.print_exc()

        return {
            "error": str(e)
        }
