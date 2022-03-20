import json
import unittest

from functions.watcher.services import ec2, lambda_, s3


class EC2Test(unittest.TestCase):

    def test_create_security_group(self):
        with open('./samples/ec2_CreateSecurityGroup.json') as f:
            data = json.loads(f.read())

        result = ec2.process_event(data)

        self.assertEqual(result['resource_id'], ['sg-YOUR_SECURITY_GROUP_ID'])
        self.assertEqual(result['identity'], 'user/test')
        self.assertEqual(result['region'], 'ap-northeast-2')
        self.assertEqual(result['event_name'], 'CreateSecurityGroup')
        self.assertEqual(result['source_ip_address'], '172.0.0.1')
        self.assertEqual(result['event_source'], 'ec2')

    def test_run_instances_single(self):
        with open('./samples/ec2_RunInstances_single.json') as f:
            data = json.loads(f.read())

        result = ec2.process_event(data)

        self.assertEqual(result['resource_id'], ['i-YOUR_INSTANCE_IDS'])
        self.assertEqual(result['identity'], 'user/test')
        self.assertEqual(result['region'], 'ap-northeast-2')
        self.assertEqual(result['event_name'], 'RunInstances')
        self.assertEqual(result['source_ip_address'], '172.0.0.1')
        self.assertEqual(result['event_source'], 'ec2')

    def test_run_instances_multi(self):
        with open('./samples/ec2_RunInstances_multi.json') as f:
            data = json.loads(f.read())

        result = ec2.process_event(data)

        self.assertEqual(result['resource_id'], ['i-YOUR_INSTANCE_IDS', 'i-YOUR_INSTANCE_IDS'])
        self.assertEqual(result['identity'], 'user/test')
        self.assertEqual(result['region'], 'ap-northeast-2')
        self.assertEqual(result['event_name'], 'RunInstances')
        self.assertEqual(result['source_ip_address'], 'AWS Internal')
        self.assertEqual(result['event_source'], 'ec2')


class LambdaTest(unittest.TestCase):
    def test_create_function_20150331(self):
        with open('./samples/lambda_CreateFunction20150331.json') as f:
            data = json.loads(f.read())

        result = lambda_.process_event(data)

        self.assertEqual(result['resource_id'], ['cloudtrailwatcher-000000000000'])
        self.assertEqual(result['identity'], 'user/test')
        self.assertEqual(result['region'], 'ap-northeast-2')
        self.assertEqual(result['event_name'], 'CreateFunction20150331')
        self.assertEqual(result['source_ip_address'], '172.0.0.1')
        self.assertEqual(result['event_source'], 'lambda')


class S3Test(unittest.TestCase):
    def test_create_bucket(self):
        with open('./samples/s3_CreateBucket.json') as f:
            data = json.loads(f.read())

        result = s3.process_event(data)

        self.assertEqual(result['resource_id'], ['cloudtrailwatcher-000000000000'])
        self.assertEqual(result['identity'], 'user/test')
        self.assertEqual(result['region'], 'ap-northeast-2')
        self.assertEqual(result['event_name'], 'CreateBucket')
        self.assertEqual(result['source_ip_address'], '172.0.0.1')
        self.assertEqual(result['event_source'], 's3')