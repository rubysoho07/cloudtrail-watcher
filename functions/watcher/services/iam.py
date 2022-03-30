import boto3

from botocore.exceptions import ClientError

from services.common import *


iam = boto3.client('iam')


def _process_create_user(event: dict, set_tag: bool = False) -> list:
    """ Process CreateUser event. """

    user_name = event['responseElements']['user']['userName']

    if set_tag is True:
        try:
            tags = iam.list_user_tags(UserName=user_name)['Tags']

            if check_contain_mandatory_tag_list(tags) is False:
                iam.tag_user(UserName=user_name,
                             Tags=[{
                                 'Key': 'User',
                                 'Value': get_user_identity(event)
                             }])
        except ClientError as ce:
            print(ce.response)
            print(f"event ID: {event['eventID']}, event name: {event['eventName']}")

    return [user_name]


def _process_create_role(event: dict, set_tag: bool = False) -> list:
    """ Process CreateRole event. """

    role_name = event['responseElements']['role']['arn'].split(':')[-1]

    if set_tag is True:
        try:
            tags = iam.list_role_tags(RoleName=role_name.split('/')[-1])['Tags']

            if check_contain_mandatory_tag_list(tags) is False:
                iam.tag_role(RoleName=role_name.split('/')[-1],
                             Tags=[{
                                 'Key': 'User',
                                 'Value': get_user_identity(event)
                             }])
        except ClientError as ce:
            print(ce.response)
            print(f"event ID: {event['eventID']}, event name: {event['eventName']}")

    return [role_name]


def _process_create_policy(event: dict, set_tag: bool = False) -> list:
    """ Process CreatePolicy event. """

    if set_tag is True:
        try:
            policy_arn = event['responseElements']['policy']['arn']

            tags = iam.list_policy_tags(PolicyArn=policy_arn)['Tags']

            if check_contain_mandatory_tag_list(tags) is False:
                iam.tag_policy(PolicyArn=policy_arn,
                               Tags=[{
                                   'Key': 'User',
                                   'Value': get_user_identity(event)
                               }])
        except ClientError as ce:
            print(ce.response)
            print(f"event ID: {event['eventID']}, event name: {event['eventName']}")

    return [event['responseElements']['policy']['policyName']]


def _process_create_instance_profile(event: dict, set_tag: bool = False) -> list:
    """ Process CreateInstanceProfile event. """

    instance_profile_name = event['responseElements']['instanceProfile']['instanceProfileName']

    if set_tag is True:
        try:
            tags = iam.list_instance_profile_tags(InstanceProfileName=instance_profile_name)['Tags']

            if check_contain_mandatory_tag_list(tags) is False:
                iam.tag_instance_profile(InstanceProfileName=instance_profile_name,
                                         Tags=[{
                                             'Key': 'User',
                                             'Value': get_user_identity(event)
                                         }])
        except ClientError as ce:
            print(ce.response)
            print(f"event ID: {event['eventID']}, event name: {event['eventName']}")

    return [instance_profile_name]


def _process_create_policy_version(event: dict) -> list:
    """ Process CreatePolicyVersion event. This function doesn't set tags. """

    policy_name = event['requestParameters']['policyArn'].split('/')[-1]
    policy_new_version = event['responseElements']['policyVersion']['versionId']

    return [f"{policy_name}:{policy_new_version}"]


def _process_create_group(event: dict) -> list:
    """ Process CreateGroup event. This function doesn't set tags. """

    return [event['responseElements']['group']['groupName']]


def process_event(event: dict) -> dict:
    """ Process CloudTrail event for IAM services """

    result = {
        "resource_id": None,
        "identity": get_user_identity(event),
        "region": event['awsRegion'],
        "source_ip_address": event['sourceIPAddress'],
        "event_name": event['eventName'],
        "event_source": get_service_name(event)
    }

    if event['responseElements'] is None:
        result['error'] = f"response is None: check CloudTrail event - {event['eventID']}"
        return result

    set_tag = check_set_mandatory_tag()

    if event['eventName'] == "CreateUser":
        result['resource_id'] = _process_create_user(event, set_tag)
    elif event['eventName'] == "CreateRole":
        result['resource_id'] = _process_create_role(event, set_tag)
    elif event['eventName'] == "CreatePolicy":
        result['resource_id'] = _process_create_policy(event, set_tag)
    elif event['eventName'] == "CreateInstanceProfile":
        result['resource_id'] = _process_create_instance_profile(event, set_tag)
    elif event['eventName'] == "CreatePolicyVersion":
        result['resource_id'] = _process_create_policy_version(event)
    elif event['eventName'] == "CreateGroup":
        result['resource_id'] = _process_create_group(event)
    else:
        message = f"Cannot process event: {event['eventName']}, eventID: f{event['eventID']}"
        print(message)
        result['error'] = message

    return result