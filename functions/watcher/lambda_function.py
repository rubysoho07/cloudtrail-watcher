import os
import gzip
import json
import importlib
import traceback

import boto3
import requests

from services import common


s3 = boto3.client('s3')
sns = boto3.resource('sns')


def process_event_by_service(record: dict) -> dict:
    """ Process event by service name"""

    service_name = common.get_service_name(record)
    try:
        if service_name == 'lambda':
            service_name = 'lambda_'

        module = importlib.import_module(f"services.{service_name}")
        return module.process_event(record)
    except ImportError:
        return {"error": f"Not supported service: {service_name}, Event ID: {record['eventID']}"}


def _convert_to_slack_message(summary: dict) -> dict:
    """ Convert summary dict to Slack message format """

    return {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f":warning: *{summary['identity']}* created new resources on "
                            f"*{summary['account_id']}:{summary['region']}*."
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": f"service: {summary['event_source']} / event_name: {summary['event_name']} "
                            f"/ source_ip: {summary['source_ip_address']} / resource_ids: {summary['resource_id']}",
                    "emoji": True
                }
            }
        ]
    }


def notify_slack(summary: dict):
    """ Send notification to Slack Webhook. """

    message = _convert_to_slack_message(summary)

    if 'SLACK_WEBHOOK_URL' in os.environ.keys() and os.environ['SLACK_WEBHOOK_URL'] != 'DISABLED':
        requests.post(os.environ['SLACK_WEBHOOK_URL'],
                      data=json.dumps(message, ensure_ascii=False),
                      headers={'Content-Type': 'application/json'})


def notify_sns(summary: dict):
    """ Send notification to SNS topic """
    if 'SNS_TOPIC_ARN' not in os.environ.keys():
        raise ValueError('SNS Topic not found')

    topic = sns.Topic(os.environ['SNS_TOPIC_ARN'])
    topic.publish(Message=json.dumps(summary))


def handler(event, context):
    print(event)
    record = None

    # Get object information
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    # Transform raw data to dict type
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        data = json.load(gzip.GzipFile(fileobj=response['Body']))

        # Check each event
        for record in data['Records']:
            if record['readOnly'] is True:
                continue

            # Process event
            result = process_event_by_service(record)

            # Add account ID information
            if 'recipientAccountId' in record.keys():
                result['account_id'] = record['recipientAccountId']
            else:
                result['account_id'] = None

            if 'error' in result.keys():
                print(json.dumps(result, ensure_ascii=False))
                continue

            # Send notification
            notify_slack(result)
            notify_sns(result)

        return {'message': event}
    except Exception as e:
        traceback.print_exc()
        if record is not None:
            print(f"Cannot process event record: ID - {record['eventID']}, eventName: {record['eventName']}")
        return {
            "error": str(e)
        }
