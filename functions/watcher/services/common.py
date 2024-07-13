import os

def get_service_name(event: dict) -> str:
    """ Get AWS service name from CloudTrail event. """
    return event['eventSource'].split('.')[0]

def get_user_identity(event: dict) -> str:
    """ Get user identity from CloudTrail event. """
    if 'arn' not in event['userIdentity'].keys():
        return "Unknown"
    return event['userIdentity']['arn'].split(':')[-1]

def check_set_mandatory_tag() -> bool:
    """
    Check if watcher function sets mandatory tags for new resources.
    If you want to set required tags, set environment variable named 'SET_MANDATORY_TAG'
    """
    return os.getenv('SET_MANDATORY_TAG', 'False').lower() not in ['disabled', 'false', '0']

def check_contain_mandatory_tag_list(tags: list) -> bool:
    """
    Check if mandatory tag exists in tag list.
    In tag list, a tag contains a key-value pair.
    for example:
    {
        "Key": "ExampleKey",
        "Value": "Example_Value"
    }
    """
    return any(tag.get('Key') == 'User' or tag.get('key') == 'User' for tag in tags)

def check_contain_mandatory_tag_dict(tags: dict) -> bool:
    """
    Check if mandatory tag exists in tag dictionary.
    In tag dict, a tag contains a key-value pair.
    for example:
    {
        "Key": "Value"
    }
    """
    return 'User' in tags

def check_disable_autoscaling_alarm() -> bool:
    """
    Check if watcher function notifies for autoscaling.
    If you want to set this feature, set environment variable named 'DISABLE_AUTOSCALING_ALARM'
    """
    return os.getenv('DISABLE_AUTOSCALING_ALARM', 'False').lower() not in ['disabled', 'false', '0']
