import json

from cloudtrail_watcher.utils import build_result, notify_slack


class TestProcessEvent:
    _account_info = ("test", "000000000000")

    def test_create_bucket(self):
        with open("test/services/samples/s3_CreateBucket.json") as f:
            data = json.loads(f.read())

        result = build_result(data)

        assert result["resource_id"] == ["cloudtrailwatcher-000000000000"]
        assert result["identity"] == "user/test"
        assert result["region"] == "ap-northeast-2"
        assert result["event_name"] == "CreateBucket"
        assert result["source_ip_address"] == "172.0.0.1"
        assert result["event_source"] == "s3"

    def test_console_login(self):
        with open("test/services/samples/signin_ConsoleLogin.json") as f:
            data = json.loads(f.read())

        result = build_result(data)

        assert result["resource_id"] == ["Success"]
        assert result["identity"] == "user/test"
        assert result["region"] == "us-east-1"
        assert result["event_name"] == "ConsoleLogin"
        assert result["source_ip_address"] == "172.0.0.1"
        assert result["event_source"] == "signin"

    def test_send_event_message(self):
        with open("test/services/samples/s3_CreateBucket.json") as f:
            data = json.loads(f.read())

        result = build_result(data)
        result["account_id"] = "000000000000"

        notify_slack(result, self._account_info)
        assert True

    def test_send_console_login_message(self):
        with open("test/services/samples/signin_ConsoleLogin.json") as f:
            data = json.loads(f.read())

        result = build_result(data)
        result["account_id"] = "000000000000"

        notify_slack(result, self._account_info)
        assert True
