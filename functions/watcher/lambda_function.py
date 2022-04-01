import os
import gzip
import json
import importlib
import traceback

from typing import Union
from urllib import request

import boto3

from botocore.exceptions import ClientError

from services import common


s3 = boto3.client('s3')
sns = boto3.resource('sns')

account_alias = (None, False)


def _get_account_alias() -> Union[tuple[str, bool], tuple[None, bool]]:
    """
        Get alias of AWS account.
        Return alias name in string and checked marker in bool type.
        If an alias is not associated with your account, alias name will be None.
    """

    iam = boto3.client('iam')

    result = iam.list_account_aliases()

    if len(result['AccountAliases']) == 0:
        return None, True
    else:
        return result['AccountAliases'][0], True


def process_console_login(record: dict) -> dict:
    """ Process ConsoleLogin event """

    return {
        "resource_id": [record['responseElements']['ConsoleLogin']],
        "identity": common.get_user_identity(record),
        "region": record['awsRegion'],
        "source_ip_address": record['sourceIPAddress'],
        "event_name": record['eventName'],
        "event_source": common.get_service_name(record)
    }


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
    global account_alias

    result = {
        "blocks": [{
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": ""
            }
        }]
    }

    if account_alias[0] is None:
        account_str = f"{summary['account_id']}"
    else:
        account_str = f"{account_alias[0]}({summary['account_id']})"

    if summary['event_name'] == 'ConsoleLogin':
        message = f":warning: *{summary['identity']}* logged in *{account_str}* " \
                  f"({summary['resource_id'][0]} / from {summary['source_ip_address']})"
        result['blocks'][0]['text']['text'] = message
    else:
        message = f":warning: *{summary['identity']}* created new resources on " \
                  f"*{account_str}:{summary['region']}*."
        result['blocks'][0]['text']['text'] = message
        # noinspection PyTypeChecker
        result['blocks'].append({
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": f"service: {summary['event_source']} / event_name: {summary['event_name']} "
                            f"/ source_ip: {summary['source_ip_address']} / resource_ids: {summary['resource_id']}",
                    "emoji": True
                }
            })

    return result


def notify_slack(summary: dict):
    """ Send notification to Slack Webhook. """

    message = _convert_to_slack_message(summary)

    if 'SLACK_WEBHOOK_URL' in os.environ.keys() and os.environ['SLACK_WEBHOOK_URL'] != 'DISABLED':
        req = request.Request(url=os.environ['SLACK_WEBHOOK_URL'],
                              data=json.dumps(message, ensure_ascii=False).encode(),
                              headers={'Content-Type': 'application/json'},
                              method='POST')
        request.urlopen(req)


def notify_sns(summary: dict):
    """ Send notification to SNS topic """
    if 'SNS_TOPIC_ARN' not in os.environ.keys():
        raise ValueError('SNS Topic not found')

    topic = sns.Topic(os.environ['SNS_TOPIC_ARN'])
    topic.publish(Message=json.dumps(summary))


def handler(event, context):
    global account_alias
    print(event)

    if account_alias[1] is False:
        account_alias = _get_account_alias()

    # Get object information
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    # Transform raw data to dict type
    response = s3.get_object(Bucket=bucket, Key=key)
    data = json.load(gzip.GzipFile(fileobj=response['Body']))

    # Check each event
    for record in data['Records']:
        try:
            if record['readOnly'] is True:
                continue

            if record['eventName'] == 'ConsoleLogin':
                result = process_console_login(record)
            else:
                # Process event
                result = process_event_by_service(record)

            # Add account ID information
            if 'recipientAccountId' in record.keys():
                result['account_id'] = record['recipientAccountId']
            else:
                result['account_id'] = None

            if 'error' in result.keys():
                # Skip to send notification
                continue

            # Send notification
            notify_slack(result)
            notify_sns(result)
        except ClientError as ce:
            print(f"(ClientError) event ID: {event['eventID']}, event name: {event['eventName']}, "
                  f"error code: {ce.response['Error']['Code']}, error message: {ce.response['Error']['Message']}")
        except Exception as e:
            traceback.print_exc()
            if record is not None:
                print(f"(Cannot process event record) event ID: {record['eventID']}, eventName: {record['eventName']}, "
                      f"Error: {e}")

    return {'message': event}
