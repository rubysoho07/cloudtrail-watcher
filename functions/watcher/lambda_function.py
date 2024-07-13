import os
import gzip
import json
import importlib
import traceback

from typing import Union
from urllib import request

import boto3
from botocore.exceptions import ClientError

from services import common, ec2

s3 = boto3.client('s3')

account_alias = (None, False)
set_tags = False

def _get_account_alias() -> Union[tuple[str, bool], tuple[None, bool]]:
    iam = boto3.client('iam')
    result = iam.list_account_aliases()
    return (result['AccountAliases'][0], True) if result['AccountAliases'] else (None, True)

def process_event_by_service(record: dict) -> dict:
    global set_tags
    service_name = common.get_service_name(record)
    try:
        if service_name == 'lambda':
            service_name = 'lambda_'
        module = importlib.import_module(f"services.{service_name}")
        return module.process_event(record, set_tags)
    except ImportError:
        return {"error": f"Not supported service: {service_name}, Event ID: {record['eventID']}"}

def _convert_to_slack_message(summary: dict) -> dict:
    global account_alias
    account_str = f"{account_alias[0]}({summary['account_id']})" if account_alias[0] else f"{summary['account_id']}"
    message = ec2.generate_message(summary)
    result = {
        "blocks": [{
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": message
            }
        }]
    }
    return result

def notify_slack(summary: dict):
    message = _convert_to_slack_message(summary)
    if os.getenv('SLACK_WEBHOOK_URL') and os.getenv('SLACK_WEBHOOK_URL') != 'DISABLED':
        req = request.Request(url=os.getenv('SLACK_WEBHOOK_URL'),
                              data=json.dumps(message, ensure_ascii=False).encode(),
                              headers={'Content-Type': 'application/json'},
                              method='POST')
        request.urlopen(req)

def build_result(record: dict) -> dict:
    result = process_event_by_service(record)
    result['event_name'] = record['eventName']
    result['source_ip_address'] = record['sourceIPAddress']
    result['identity'] = common.get_user_identity(record).replace('user/', '')
    result['region'] = record['awsRegion']
    result['event_source'] = common.get_service_name(record)
    result['account_id'] = record.get('recipientAccountId', None)
    if 'errorCode' in record:
        result['error_code'] = record['errorCode']
        result['error_message'] = record.get('errorMessage', 'No error message provided')
    if record['eventName'] in ['AuthorizeSecurityGroupIngress', 'AuthorizeSecurityGroupEgress']:
        result['ip_permissions'] = []
        for item in record['requestParameters']['ipPermissions']['items']:
            permission = {
                'ipProtocol': item.get('ipProtocol', 'N/A'),
                'fromPort': item.get('fromPort', 'N/A'),
                'toPort': item.get('toPort', 'N/A'),
                'cidrIp': item['ipRanges']['items'][0].get('cidrIp', 'N/A') if item['ipRanges']['items'] else 'N/A',
                'description': item['ipRanges']['items'][0].get('description', 'N/A') if item['ipRanges']['items'] else 'N/A'
            }
            result['ip_permissions'].append(permission)
    elif record['eventName'] in ['RevokeSecurityGroupIngress', 'RevokeSecurityGroupEgress']:
        result['ip_permissions'] = []
        for item in record['responseElements']['revokedSecurityGroupRuleSet']['items']:
            permission = {
                'ipProtocol': item.get('ipProtocol', 'N/A'),
                'fromPort': item.get('fromPort', 'N/A'),
                'toPort': item.get('toPort', 'N/A'),
                'cidrIp': item.get('cidrIpv4', 'N/A'),
                'description': item.get('description', 'N/A')
            }
            result['ip_permissions'].append(permission)
    return result

def handler(event, context):
    global account_alias
    global set_tags
    print(event)
    if not account_alias[1]:
        account_alias = _get_account_alias()
    set_tags = common.check_set_mandatory_tag()
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    response = s3.get_object(Bucket=bucket, Key=key)
    data = json.load(gzip.GzipFile(fileobj=response['Body']))
    for record in data['Records']:
        try:
            if record.get('readOnly'):
                continue
            result = build_result(record)
            if 'error' in result:
                continue
            notify_slack(result)
        except ClientError as ce:
            print(f"(ClientError) event ID: {record['eventID']}, event name: {record['eventName']}, "
                  f"error code: {ce.response['Error']['Code']}, error message: {ce.response['Error']['Message']}")
        except Exception as e:
            traceback.print_exc()
            print(f"(Cannot process event record) event ID: {record['eventID']}, eventName: {record['eventName']}, Error: {e}")
    return {'message': event}
