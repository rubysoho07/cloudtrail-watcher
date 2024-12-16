import boto3
from services.common import get_user_identity

ec2 = boto3.resource('ec2')

def _get_instance_resource_ids(event: dict) -> list:
    return [instance['instanceId'] for instance in event['responseElements']['instancesSet']['items']]

def _check_instance_tag_requests(tags: dict, result: dict):
    for item in tags.get('items', []):
        for tag in item.get('tags', []):
            if tag['key'] == 'User' and item['resourceType'] in result:
                result[item['resourceType']] = True

def process_run_instances(event: dict, set_tags: bool = False) -> list:
    resource_ids = _get_instance_resource_ids(event)
    if set_tags:
        has_user_tag = {'instance': False, 'volume': False, 'network-interface': False}
        common_tags = [{'Key': 'User', 'Value': get_user_identity(event)}]
        if 'tagSpecificationSet' in event['requestParameters']:
            _check_instance_tag_requests(event['requestParameters']['tagSpecificationSet'], has_user_tag)
        for resource_id in resource_ids:
            instance = ec2.Instance(resource_id)
            if not has_user_tag['instance']:
                instance.create_tags(Tags=common_tags)
            if not has_user_tag['volume']:
                for volume in instance.volumes.all():
                    volume.create_tags(Tags=common_tags)
            if not has_user_tag['network-interface'] and instance.network_interfaces:
                for eni in instance.network_interfaces:
                    eni.create_tags(Tags=common_tags)
    return resource_ids

def process_create_security_group(event: dict, set_tag: bool = False) -> list:
    resource_ids = [event['responseElements']['groupId']]
    if set_tag:
        sg = ec2.SecurityGroup(resource_ids[0])
        if not any(tag['Key'] == 'User' for tag in sg.tags or []):
            sg.create_tags(Tags=[{'Key': 'User', 'Value': get_user_identity(event)}])
    return resource_ids

def process_modify_security_group(event: dict) -> list:
    return [event['requestParameters']['groupId']]

def process_create_key_pair(event: dict) -> list:
    return [event['responseElements']['keyName']]

def process_create_image(event: dict) -> list:
    return [event['responseElements']['imageId']]

def process_event(event: dict, set_tag: bool = False) -> dict:
    result = dict()
    if not event.get('responseElements'):
        result['error'] = f"response is null: eventName - {event['eventName']}, eventID: {event['eventID']}"
        return result
    if event['eventName'] == "RunInstances":
        result['resource_id'] = process_run_instances(event, set_tag)
    elif event['eventName'] == "CreateSecurityGroup":
        result['resource_id'] = process_create_security_group(event, set_tag)
    elif event['eventName'] in ["AuthorizeSecurityGroupIngress", "AuthorizeSecurityGroupEgress", "RevokeSecurityGroupIngress", "RevokeSecurityGroupEgress"]:
        result['resource_id'] = process_modify_security_group(event)
    elif event['eventName'] == "CreateKeyPair":
        result['resource_id'] = process_create_key_pair(event)
    elif event['eventName'] == "CreateImage":
        result['resource_id'] = process_create_image(event)
    else:
        result['error'] = f"Cannot process event: {event['eventName']}, eventID: {event['eventID']}"
    return result

def generate_message(summary: dict) -> str:
    service_name_map = {
        'Instance': 'EC2',
        'SecurityGroup': 'Security Group',
        'Image': 'AMI',
        'Volume': 'EBS',
        'KeyPair': 'KeyPair'
    }

    event_name_map = {
        'CreateSecurityGroup': '보안그룹 생성',
        'RunInstances': 'EC2 생성',
        'CreateImage': 'AMI 생성',
        'CreateKeyPair': 'KeyPair 생성',
        'AuthorizeSecurityGroupIngress': '인바운드룰 추가',
        'AuthorizeSecurityGroupEgress': '인바운드룰 삭제',
        'RevokeSecurityGroupIngress': '아웃바운드룰 추가',
        'RevokeSecurityGroupEgress': '아웃바운드룰 삭제',
        'StopInstances': 'EC2 중지',
        'StartInstances': 'EC2 시작',
        'AttachVolume': 'EBS 부착',
        'DetachVolume': 'EBS 제거',
        'DeleteSecurityGroup': '보안그룹 삭제',
        'TerminateInstances': 'EC2 삭제',
        'DeleteVolume': 'EBS 삭제',
        'DeregisterImage': 'AMI 삭제',
        'DeleteKeyPair': 'KeyPair 삭제'
    }

    user_identity = summary['identity'].replace('user/', '')
    event_name = summary['event_name']
    service = summary['event_source']
    resource_ids = summary['resource_id']

    service_display = next((name for key, name in service_name_map.items() if key in event_name), service)
    event_display = event_name_map.get(event_name, event_name)

    if event_name in ['CreateSecurityGroup', 'RunInstances', 'CreateImage', 'CreateKeyPair']:
        message = f":white_check_mark: *{user_identity}* (이)가 리소스를 생성하였습니다.\n" \
                f"- 서비스: {service_display}\n" \
                f"- 이벤트 이름: {event_display}\n" \
                f"- 리소스 ID: {resource_ids}"
    elif event_name in ['AuthorizeSecurityGroupIngress', 'AuthorizeSecurityGroupEgress', 'RevokeSecurityGroupIngress', 'RevokeSecurityGroupEgress']:
        message = f":information_source: *{user_identity}* (이)가 보안그룹 룰을 수정하였습니다.\n" \
                f"- 서비스: {service_display}\n" \
                f"- 이벤트 이름: {event_display}\n" \
                f"- 리소스 ID: {resource_ids}"
        ip_permissions = summary.get('ip_permissions', [])
        for permission in ip_permissions:
            ip = permission.get('cidrIp', 'N/A')
            protocol = permission.get('ipProtocol', 'N/A')
            port = permission.get('toPort', 'N/A')
            description = permission.get('description', 'N/A')
            message += f"\n    - IP: {ip}\n    - Protocol: {protocol}\n    - Port: {port}\n    - Description: {description}"
    elif event_name in ['StopInstances', 'StartInstances']:
        message = f":information_source: *{user_identity}* (이)가 인스턴스 상태를 변경하였습니다.\n" \
                f"- 서비스: {service_display}\n" \
                f"- 이벤트 이름: {event_display}\n" \
                f"- 리소스 ID: {resource_ids}"
    elif event_name in ['AttachVolume', 'DetachVolume']:
        message = f":information_source: *{user_identity}* (이)가 EBS를 수정하였습니다.\n" \
                f"- 서비스: {service_display}\n" \
                f"- 이벤트 이름: {event_display}\n" \
                f"- 리소스 ID: {resource_ids}"
    elif event_name in ['DeleteSecurityGroup', 'TerminateInstances', 'DeleteVolume', 'DeregisterImage', 'DeleteKeyPair']:
        message = f":x: *{user_identity}* (이)가 리소스를 삭제하였습니다.\n" \
                f"- 서비스: {service_display}\n" \
                f"- 이벤트 이름: {event_display}\n" \
                f"- 리소스 ID: {resource_ids}"
    else:
        message = f":grey_question: *{user_identity}* (이)가 작업을 수행하였습니다.\n" \
                f"- 서비스: {service_display}\n" \
                f"- 이벤트 이름: {event_display}\n" \
                f"- 리소스 ID: {resource_ids}"

    if 'error_code' in summary:
        error_message = summary.get('error_message', 'Cannot found error message')
        message += f"\n오류 발생: \n- 오류 코드: {summary['error_code']}\n- 오류 메시지: {error_message}"

    return message
