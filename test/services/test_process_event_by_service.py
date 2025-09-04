import json
import unittest

from layer.python.cloudtrail_watcher.utils import build_result, notify_slack


class ProcessEventTest(unittest.TestCase):

    _account_info = ("test", "000000000000")

    def test_create_bucket(self):
        with open('./samples/s3_CreateBucket.json') as f:
            data = json.loads(f.read())

        result = build_result(data)

        self.assertEqual(result['resource_id'], ['cloudtrailwatcher-000000000000'])
        self.assertEqual(result['identity'], 'user/test')
        self.assertEqual(result['region'], 'ap-northeast-2')
        self.assertEqual(result['event_name'], 'CreateBucket')
        self.assertEqual(result['source_ip_address'], '172.0.0.1')
        self.assertEqual(result['event_source'], 's3')

    def test_console_login(self):
        with open('samples/signin_ConsoleLogin.json') as f:
            data = json.loads(f.read())

        result = build_result(data)

        self.assertEqual(result['resource_id'], ["Success"])
        self.assertEqual(result['identity'], 'user/test')
        self.assertEqual(result['region'], 'us-east-1')
        self.assertEqual(result['event_name'], 'ConsoleLogin')
        self.assertEqual(result['source_ip_address'], '172.0.0.1')
        self.assertEqual(result['event_source'], 'signin')

    def test_send_event_message(self):
        with open('./samples/s3_CreateBucket.json') as f:
            data = json.loads(f.read())

        result = build_result(data)
        result['account_id'] = '000000000000'

        notify_slack(result, self._account_info)
        self.assertTrue(True)

    def test_send_console_login_message(self):
        with open('samples/signin_ConsoleLogin.json') as f:
            data = json.loads(f.read())

        result = build_result(data)
        result['account_id'] = '000000000000'

        notify_slack(result, self._account_info)
        self.assertTrue(True)
