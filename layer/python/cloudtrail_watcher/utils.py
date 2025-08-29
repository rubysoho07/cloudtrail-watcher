import os
import json
import boto3
import importlib

from typing import Union
from urllib import request

from .services import common

sns = boto3.resource('sns')

def get_account_alias() -> Union[tuple[str, bool], tuple[None, bool]]:
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
        message = f":warning: *{summary['identity']}* logged in *{account_str}* \n" \
                  f"Status: {summary['resource_id'][0]}\n" \
                  f"Source IP: {summary['source_ip_address']}"
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
                    "text": f"- Service: {summary['event_source']}\n"
                            f"- Event name: {summary['event_name']}\n"
                            f"- Source IP: {summary['source_ip_address']}\n"
                            f"- Resource IDs: {summary['resource_id']}",
                    "emoji": True
                }
            })

    if 'error_code' in summary.keys():
        if 'error_message' in summary.keys():
            error_message = summary['error_message']
        else:
            error_message = 'Cannot found error message'

        result['blocks'].append({
            "type": "section",
            "text": {
                "type": "plain_text",
                "text": f"Error occurred : \n"
                        f"- Error Code: {summary['error_code']}\n"
                        f"- Error Message: {error_message}\n",
                "emoji": True
            }
        })

    return result


def process_event_by_service(record: dict) -> dict:
    """ Process event by service name"""
    global set_tags

    service_name = common.get_service_name(record)
    try:
        if service_name == 'lambda':
            service_name = 'lambda_'

        module = importlib.import_module(f".services.{service_name}")
        return module.process_event(record, set_tags)
    except ImportError:
        return {"error": f"Not supported service: {service_name}, Event ID: {record['eventID']}"}


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


def build_result(record: dict) -> dict:
    """ Build result dictionary from CloudTrail Event. """
    if record['eventName'] == 'ConsoleLogin':
        result = {
            "resource_id": [record['responseElements']['ConsoleLogin']]
        }
    else:
        result = process_event_by_service(record)

    result['event_name'] = record['eventName']
    result['source_ip_address'] = record['sourceIPAddress']
    result['identity'] = common.get_user_identity(record)
    result['region'] = record['awsRegion']

    if 'event_source' not in result.keys():
        result['event_source'] = common.get_service_name(record)

    # Add account ID information
    if 'recipientAccountId' in record.keys():
        result['account_id'] = record['recipientAccountId']
    else:
        result['account_id'] = None

    # If error occurred, add error information
    if 'errorCode' in record.keys():
        result['error_code'] = result['errorCode']

        if 'errorMessage' in record.keys():
            result['error_message'] = result['errorMessage']

    return result