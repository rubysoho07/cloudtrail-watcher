import boto3

from services.common import *

elb = boto3.client('elb')
elb_v2 = boto3.client('elbv2')


def _process_create_load_balancer(event: dict, set_tags: bool = False) -> list:

    is_clb = 'type' not in event['requestParameters']

    if set_tags is True:
        if is_clb is True:
            response = elb.describe_tags(LoadBalancerNames=[event['requestParameters']['loadBalancerName']])
        else:
            response = elb_v2.describe_tags(
                ResourceArns=[event['responseElements']['loadBalancers'][0]['loadBalancerArn']]
            )

        exists_mandatory_tags = check_contain_mandatory_tag_list(response['TagDescriptions'][0]['Tags'])

        if exists_mandatory_tags is False:
            if is_clb is True:
                elb.add_tags(
                    LoadBalancerNames=[event['requestParameters']['loadBalancerName']],
                    Tags=[{
                        'Key': 'User',
                        'Value': get_user_identity(event)
                    }]
                )
            else:
                elb_v2.add_tags(
                    ResourceArns=[event['responseElements']['loadBalancers'][0]['loadBalancerArn']],
                    Tags=[{
                        'Key': 'User',
                        'Value': get_user_identity(event)
                    }]
                )

    if is_clb is True:        # ALB, NLB, GLB
        return [event['requestParameters']['loadBalancerName']]
    else:                     # CLB
        return [event['requestParameters']['name']]


def process_event(event: dict, set_tag: bool = False) -> dict:
    """ Process CloudTrail event for ELB """

    result = dict()

    if event['eventName'] == "CreateLoadBalancer":
        result['resource_id'] = _process_create_load_balancer(event, set_tag)
    else:
        message = f"Cannot process event: {event['eventName']}, eventID: {event['eventID']}"
        result['error'] = message

    return result
