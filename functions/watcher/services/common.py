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
    if 'SET_MANDATORY_TAG' in os.environ.keys() and \
       os.environ['SET_MANDATORY_TAG'] not in ['DISABLED', 'False', '0', 'false']:
        return True

    return False
