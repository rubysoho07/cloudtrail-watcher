import json
import unittest

from functions.watcher.lambda_function import process_event_by_service


class ProcessEventTest(unittest.TestCase):
    def test_create_bucket(self):
        with open('./samples/s3_CreateBucket.json') as f:
            data = json.loads(f.read())

        result = process_event_by_service(data)

        self.assertEqual(result['resource_id'], ['cloudtrailwatcher-000000000000'])
        self.assertEqual(result['identity'], 'user/test')
        self.assertEqual(result['region'], 'ap-northeast-2')
        self.assertEqual(result['event_name'], 'CreateBucket')
        self.assertEqual(result['source_ip_address'], '172.0.0.1')
        self.assertEqual(result['event_source'], 's3')