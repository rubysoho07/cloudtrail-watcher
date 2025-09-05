# Lambda Layer in Python

## Purpose

This rule manages features to process CloudTrail log by event name.

## Instructions

* Please refer the rule of a CloudTrail event: https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-events.html
* Get AWS service name from `eventSource` in the event. If `eventSource` is "cloudtrail.amazonaws.com", use "cloudtrail" before "amazonaws.com". (ID: SERVICE_NAME)
* Create a file if `layer/python/cloudtrail_watcher/services/SERVICE_NAME.py` doesn't exist. File structure is below. (ID: SERVICE_FILE)

```python
import boto3

from .common import *

SERVICE_NAME = boto3.client('SERVICE_NAME')

def process_event(event: dict, set_tag: bool = False) -> dict:
    """ Process CloudTrail event for SERVICE_NAME """
	
    result = dict()

    return result
```

* Get the name of the event from `eventName` in the CloudTrail event. (ID: EVENT_NAME)
* Create a function in SERVICE_FILE.
    * Function name: Start with `_process_`, add EVENT_NAME with snake case.
    * Arguments: event in dict, set_tag in bool. The default value of set_tag is False.
    * Return value: resource name in list
    * If set_tag is True, check whether 'User' tag exists.
        * If 'User' tag doesn't exists, set 'User' tag by using 'get_user_identity' function in 'common.py'. 
* Add a rule below in process_event function.

```python
if event['eventName'] == 'EVENT_NAME':
    result['resource_id'] = "Call the function created from PROCESS_FUNCTION"
else:
    message = f"Cannot process event: {event['eventName']}, eventID: f{event['eventID']}"
    result['error'] = message
```

## Priority

High

## Error Handling

N/A