import boto3

from services.common import *

ec2 = boto3.resource('ec2')


def _get_instance_resource_ids(event: dict) -> list:
    """ Get resource id from CloudTrail event. """
    result = []

    for instance in event['responseElements']['instancesSet']['items']:
        result.append(instance['instanceId'])

    return result


def _check_instance_tag_requests(tags: dict, result: dict):
    """ Check instance tag request for instance, volume, and if 'User' tag exists. """

    if len(tags['items']) == 0:
        return

    for item in tags['items']:
        for tag in item['tags']:
            if tag['key'] == 'User':
                result[tags['resourceType']] = True


def _process_run_instances(event: dict, set_tags: bool = False) -> list:

    resource_ids = _get_instance_resource_ids(event)

    # Set mandatory tags
    if set_tags is True:
        has_user_tag = {
            'instance': False,
            'volume': False,
            'network-interface': False
        }

        common_tags = [{
            'Key': 'User',
            'Value': get_user_identity(event)
        }]

        if 'tagSpecificationSet' in event['requestParameters'].keys():
            _check_instance_tag_requests(event['requestParameters']['tagSpecificationSet'], has_user_tag)

        for resource_id in resource_ids:
            instance = ec2.Instance(resource_id)

            if has_user_tag['instance'] is False:
                instance.create_tags(Tags=common_tags)

            if has_user_tag['volume'] is False:
                for volume in instance.volumes.all():
                    volume.create_tags(Tags=common_tags)

            if has_user_tag['network-interface'] is False and instance.network_interfaces is not None:
                for eni in instance.network_interfaces:
                    eni.create_tags(Tags=common_tags)

    return resource_ids


def _process_create_security_group(event: dict, set_tag: bool = False) -> list:

    resource_ids = [event['responseElements']['groupId']]

    sg = ec2.SecurityGroup(resource_ids[0])

    if set_tag is True:
        has_user_tags = False

        # Check tags
        if sg.tags is not None:
            for tag in sg.tags:
                if tag['Key'] == 'User':
                    has_user_tags = True
                    break

        # If mandatory tags are not set, set mandatory tags
        if has_user_tags is False:
            sg.create_tags(Tags=[{
                'Key': 'User',
                'Value': get_user_identity(event)
            }])

    return resource_ids


def process_event(event: dict) -> dict:
    """ Process CloudTrail event for EC2 services """

    result = {
        "resource_id": None,
        "identity": get_user_identity(event),
        "region": event['awsRegion'],
        "source_ip_address": event['sourceIPAddress'],
        "event_name": event['eventName'],
        "event_source": get_service_name(event)
    }

    if event['responseElements'] is None:
        result['error'] = f"response is null: eventName - {event['eventName']}, eventID: {event['eventID']},"
        return result

    set_tag = check_set_mandatory_tag()

    if event['eventName'] == "RunInstances":
        result['resource_id'] = _process_run_instances(event, set_tag)
    elif event['eventName'] == "CreateSecurityGroup":
        result['resource_id'] = _process_create_security_group(event, set_tag)
    else:
        message = f"Cannot process event: {event['eventName']}, eventID: {event['eventID']}"
        result['error'] = message

    return result
