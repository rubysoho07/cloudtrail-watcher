import gzip
import json
import traceback

import boto3

from botocore.exceptions import ClientError

from cloudtrail_watcher.services import common
from cloudtrail_watcher.utils import notify_slack, notify_sns, get_account_alias, build_result


s3 = boto3.client('s3')

account_alias = (None, False)
set_tags = False
disable_autoscaling_alarm = False


def handler(event, context):
    global account_alias
    global set_tags
    global disable_autoscaling_alarm

    print(event)

    if account_alias[1] is False:
        account_alias = get_account_alias()

    set_tags = common.check_set_mandatory_tag()
    disable_autoscaling_alarm = common.check_disable_autoscaling_alarm()

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

            result = build_result(record, set_tags)

            if 'error' in result.keys():
                # Skip to send notification
                continue

            # Skip autoscaling alarm
            if disable_autoscaling_alarm and \
                    result['identity'].startswith("assumed-role/AWSServiceRoleForAutoScaling"):
                continue

            # Send notification
            notify_slack(result, account_alias)
            notify_sns(result)
        except ClientError as ce:
            print(f"(ClientError) event ID: {record['eventID']}, event name: {record['eventName']}, "
                  f"error code: {ce.response['Error']['Code']}, error message: {ce.response['Error']['Message']}")
        except Exception as e:
            traceback.print_exc()
            if record is not None:
                print(f"(Cannot process event record) event ID: {record['eventID']}, eventName: {record['eventName']}, "
                      f"Error: {e}")

    return {'message': event}
