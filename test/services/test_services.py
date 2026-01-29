import json

from cloudtrail_watcher.utils import build_result


class TestEC2:
    def test_create_security_group(self):
        with open("test/services/samples/ec2_CreateSecurityGroup.json") as f:
            data = json.loads(f.read())

        result = build_result(data)

        assert result["resource_id"] == ["sg-YOUR_SECURITY_GROUP_ID"]
        assert result["identity"] == "user/test"
        assert result["region"] == "ap-northeast-2"
        assert result["event_name"] == "CreateSecurityGroup"
        assert result["source_ip_address"] == "172.0.0.1"
        assert result["event_source"] == "ec2"

    def test_run_instances_single(self):
        with open("test/services/samples/ec2_RunInstances_single.json") as f:
            data = json.loads(f.read())

        result = build_result(data)

        assert result["resource_id"] == ["i-YOUR_INSTANCE_IDS"]
        assert result["identity"] == "user/test"
        assert result["region"] == "ap-northeast-2"
        assert result["event_name"] == "RunInstances"
        assert result["source_ip_address"] == "172.0.0.1"
        assert result["event_source"] == "ec2"

    def test_run_instances_multi(self):
        with open("test/services/samples/ec2_RunInstances_multi.json") as f:
            data = json.loads(f.read())

        result = build_result(data)

        assert result["resource_id"] == ["i-YOUR_INSTANCE_IDS", "i-YOUR_INSTANCE_IDS"]
        assert result["identity"] == "user/test"
        assert result["region"] == "ap-northeast-2"
        assert result["event_name"] == "RunInstances"
        assert result["source_ip_address"] == "AWS Internal"
        assert result["event_source"] == "ec2"

    def test_authorize_security_group_egress(self):
        with open("test/services/samples/ec2_AuthorizeSecurityGroupEgress.json") as f:
            data = json.loads(f.read())

        result = build_result(data)

        assert result["resource_id"] == ["sg-0e79c7acdf4a0225e"]
        assert result["identity"] == "user/test_user"
        assert result["region"] == "ap-northeast-2"
        assert result["event_name"] == "AuthorizeSecurityGroupEgress"
        assert result["source_ip_address"] == "127.0.0.1"
        assert result["event_source"] == "ec2"

    def test_authorize_security_group_ingress(self):
        with open("test/services/samples/ec2_AuthorizeSecurityGroupIngress.json") as f:
            data = json.loads(f.read())

        result = build_result(data)

        assert result["resource_id"] == ["sg-0e79c7acdf4a0225e"]
        assert result["identity"] == "user/test_user"
        assert result["region"] == "ap-northeast-2"
        assert result["event_name"] == "AuthorizeSecurityGroupIngress"
        assert result["source_ip_address"] == "127.0.0.1"
        assert result["event_source"] == "ec2"

    def test_revoke_security_group_egress(self):
        with open("test/services/samples/ec2_RevokeSecurityGroupEgress.json") as f:
            data = json.loads(f.read())

        result = build_result(data)

        assert result["resource_id"] == ["sg-0e79c7acdf4a0225e"]
        assert result["identity"] == "user/test_user"
        assert result["region"] == "ap-northeast-2"
        assert result["event_name"] == "RevokeSecurityGroupEgress"
        assert result["source_ip_address"] == "127.0.0.1"
        assert result["event_source"] == "ec2"

    def test_revoke_security_group_ingress(self):
        with open("test/services/samples/ec2_RevokeSecurityGroupIngress.json") as f:
            data = json.loads(f.read())

        result = build_result(data)

        assert result["resource_id"] == ["sg-0e79c7acdf4a0225e"]
        assert result["identity"] == "user/test_user"
        assert result["region"] == "ap-northeast-2"
        assert result["event_name"] == "RevokeSecurityGroupIngress"
        assert result["source_ip_address"] == "127.0.0.1"
        assert result["event_source"] == "ec2"

    def test_modify_security_group_rules(self):
        with open("test/services/samples/ec2_ModifySecurityGroupRules.json") as f:
            data = json.loads(f.read())

        result = build_result(data)

        assert result["resource_id"] == ["sg-ef6e8186"]
        assert result["identity"] == "user/test_user"
        assert result["region"] == "ap-northeast-2"
        assert result["event_name"] == "ModifySecurityGroupRules"
        assert result["source_ip_address"] == "127.0.0.1"
        assert result["event_source"] == "ec2"


class TestLambda:
    def test_create_function_20150331(self):
        with open("test/services/samples/lambda_CreateFunction20150331.json") as f:
            data = json.loads(f.read())

        result = build_result(data)

        assert result["resource_id"] == ["cloudtrailwatcher-000000000000"]
        assert result["identity"] == "user/test"
        assert result["region"] == "ap-northeast-2"
        assert result["event_name"] == "CreateFunction20150331"
        assert result["source_ip_address"] == "172.0.0.1"
        assert result["event_source"] == "lambda"


class TestS3:
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


class TestRDS:
    def test_create_db_cluster(self):
        with open("test/services/samples/rds_CreateDBCluster.json") as f:
            data = json.loads(f.read())

        result = build_result(data)

        assert result["resource_id"] == ["test-db"]
        assert result["identity"] == "user/test"
        assert result["region"] == "ap-northeast-2"
        assert result["event_name"] == "CreateDBCluster"
        assert result["source_ip_address"] == "AWS Internal"
        assert result["event_source"] == "rds"

    def test_create_db_instance(self):
        with open("test/services/samples/rds_CreateDBInstance.json") as f:
            data = json.loads(f.read())

        result = build_result(data)

        assert result["resource_id"] == ["test-db-instance-1"]
        assert result["identity"] == "user/test"
        assert result["region"] == "ap-northeast-2"
        assert result["event_name"] == "CreateDBInstance"
        assert result["source_ip_address"] == "AWS Internal"
        assert result["event_source"] == "rds"

    def test_create_db_cluster_docdb(self):
        with open("test/services/samples/rds_CreateDBCluster_DocDB.json") as f:
            data = json.loads(f.read())

        result = build_result(data)

        assert result["resource_id"] == ["ctw-test"]
        assert result["identity"] == "user/test_user"
        assert result["region"] == "ap-northeast-2"
        assert result["event_name"] == "CreateDBCluster"
        assert result["source_ip_address"] == "127.0.0.1"
        assert result["event_source"] == "documentdb"

    def test_create_db_instance_docdb(self):
        with open("test/services/samples/rds_CreateDBInstance_DocDB.json") as f:
            data = json.loads(f.read())

        result = build_result(data)

        assert result["resource_id"] == ["ctw-test"]
        assert result["identity"] == "user/test_user"
        assert result["region"] == "ap-northeast-2"
        assert result["event_name"] == "CreateDBInstance"
        assert result["source_ip_address"] == "127.0.0.1"
        assert result["event_source"] == "documentdb"


class TestElastiCache:
    def test_create_cache_cluster(self):
        with open("test/services/samples/elasticache_CreateCacheCluster.json") as f:
            data = json.loads(f.read())

        result = build_result(data)

        assert result["resource_id"] == ["test-memcached"]
        assert result["identity"] == "user/test"
        assert result["region"] == "ap-northeast-2"
        assert result["event_name"] == "CreateCacheCluster"
        assert result["source_ip_address"] == "AWS Internal"
        assert result["event_source"] == "elasticache"

    def test_create_replication_group(self):
        with open("test/services/samples/elasticache_CreateReplicationGroup.json") as f:
            data = json.loads(f.read())

        result = build_result(data)

        assert result["resource_id"] == ["test"]
        assert result["identity"] == "user/test"
        assert result["region"] == "ap-northeast-2"
        assert result["event_name"] == "CreateReplicationGroup"
        assert result["source_ip_address"] == "AWS Internal"
        assert result["event_source"] == "elasticache"


class TestEMR:
    def test_run_job_flow(self):
        with open("test/services/samples/elasticmapreduce_RunJobFlow.json") as f:
            data = json.loads(f.read())

        result = build_result(data)

        assert result["resource_id"] == ["j-2E1G6JJE6X1MQ"]
        assert result["identity"] == "user/test"
        assert result["region"] == "ap-northeast-2"
        assert result["event_name"] == "RunJobFlow"
        assert result["source_ip_address"] == "AWS Internal"
        assert result["event_source"] == "elasticmapreduce"


class TestRedshift:
    def test_create_cluster(self):
        with open("test/services/samples/redshift_CreateCluster.json") as f:
            data = json.loads(f.read())

        result = build_result(data)

        assert result["resource_id"] == ["test-goni"]
        assert result["identity"] == "user/test"
        assert result["region"] == "ap-northeast-2"
        assert result["event_name"] == "CreateCluster"
        assert result["source_ip_address"] == "AWS Internal"
        assert result["event_source"] == "redshift"


class TestECS:
    def test_create_cluster(self):
        with open("test/services/samples/ecs_CreateCluster.json") as f:
            data = json.loads(f.read())

        result = build_result(data)

        assert result["resource_id"] == ["test-ecs"]
        assert result["identity"] == "user/test"
        assert result["region"] == "ap-northeast-2"
        assert result["event_name"] == "CreateCluster"
        assert result["source_ip_address"] == "cloudformation.amazonaws.com"
        assert result["event_source"] == "ecs"


class TestEKS:
    def test_create_cluster(self):
        with open("test/services/samples/eks_CreateCluster.json") as f:
            data = json.loads(f.read())

        result = build_result(data)

        assert result["resource_id"] == ["test"]
        assert result["identity"] == "user/test"
        assert result["region"] == "ap-northeast-2"
        assert result["event_name"] == "CreateCluster"
        assert result["source_ip_address"] == "172.0.0.1"
        assert result["event_source"] == "eks"


class TestIAM:
    def test_create_user(self):
        with open("test/services/samples/iam_CreateUser.json") as f:
            data = json.loads(f.read())

        result = build_result(data)

        assert result["resource_id"] == ["test_user"]
        assert result["identity"] == "user/test"
        assert result["region"] == "us-east-1"
        assert result["event_name"] == "CreateUser"
        assert result["source_ip_address"] == "AWS Internal"
        assert result["event_source"] == "iam"

    def test_create_group(self):
        with open("test/services/samples/iam_CreateGroup.json") as f:
            data = json.loads(f.read())

        result = build_result(data)

        assert result["resource_id"] == ["test_group"]
        assert result["identity"] == "user/test"
        assert result["region"] == "us-east-1"
        assert result["event_name"] == "CreateGroup"
        assert result["source_ip_address"] == "AWS Internal"
        assert result["event_source"] == "iam"

    def test_create_policy(self):
        with open("test/services/samples/iam_CreatePolicy.json") as f:
            data = json.loads(f.read())

        result = build_result(data)

        assert result["resource_id"] == ["your_policy_name"]
        assert result["identity"] == "user/test"
        assert result["region"] == "us-east-1"
        assert result["event_name"] == "CreatePolicy"
        assert result["source_ip_address"] == "172.0.0.1"
        assert result["event_source"] == "iam"

    def test_create_role(self):
        with open("test/services/samples/iam_CreateRole.json") as f:
            data = json.loads(f.read())

        result = build_result(data)

        assert result["resource_id"] == ["role/service-role/your_role_name"]
        assert result["identity"] == "user/test"
        assert result["region"] == "us-east-1"
        assert result["event_name"] == "CreateRole"
        assert result["source_ip_address"] == "172.0.0.1"
        assert result["event_source"] == "iam"

    def test_create_policy_version(self):
        with open("test/services/samples/iam_CreatePolicyVersion.json") as f:
            data = json.loads(f.read())

        result = build_result(data)

        assert result["resource_id"] == ["test-policy:v2"]
        assert result["identity"] == "user/test"
        assert result["region"] == "us-east-1"
        assert result["event_name"] == "CreatePolicyVersion"
        assert result["source_ip_address"] == "AWS Internal"
        assert result["event_source"] == "iam"

    def test_create_instance_profile(self):
        with open("test/services/samples/iam_CreateInstanceProfile.json") as f:
            data = json.loads(f.read())

        result = build_result(data)

        assert result["resource_id"] == ["EC2_Role"]
        assert result["identity"] == "user/test"
        assert result["region"] == "us-east-1"
        assert result["event_name"] == "CreateInstanceProfile"
        assert result["source_ip_address"] == "AWS Internal"
        assert result["event_source"] == "iam"


class TestOpenSearch:
    def test_create_db_cluster(self):
        with open("test/services/samples/es_CreateDomain.json") as f:
            data = json.loads(f.read())

        result = build_result(data)

        assert result["resource_id"] == ["test-es2"]
        assert result["identity"] == "user/test"
        assert result["region"] == "ap-northeast-2"
        assert result["event_name"] == "CreateDomain"
        assert result["source_ip_address"] == "AWS Internal"
        assert result["event_source"] == "es"


class TestMSK:
    def test_create_cluster_v2(self):
        with open("test/services/samples/kafka_CreateClusterV2.json") as f:
            data = json.loads(f.read())

        result = build_result(data)

        assert result["resource_id"] == ["ct-watcher-test"]
        assert result["identity"] == "user/test_user"
        assert result["region"] == "ap-northeast-2"
        assert result["event_name"] == "CreateClusterV2"
        assert result["source_ip_address"] == "172.0.0.1"
        assert result["event_source"] == "kafka"


class TestMWAA:
    def test_create_environment(self):
        with open("test/services/samples/airflow_CreateEnvironment.json") as f:
            data = json.loads(f.read())

        result = build_result(data)

        assert result["resource_id"] == ["ct-watcher-test"]
        assert result["identity"] == "user/test_user"
        assert result["region"] == "ap-northeast-2"
        assert result["event_name"] == "CreateEnvironment"
        assert result["source_ip_address"] == "172.0.0.1"
        assert result["event_source"] == "airflow"


class TestDynamoDB:
    def test_create_table(self):
        with open("test/services/samples/dynamodb_CreateTable.json") as f:
            data = json.loads(f.read())

        result = build_result(data)

        assert result["resource_id"] == ["ct-watcher-test"]
        assert result["identity"] == "user/test_user"
        assert result["region"] == "ap-northeast-2"
        assert result["event_name"] == "CreateTable"
        assert result["source_ip_address"] == "172.0.0.1"
        assert result["event_source"] == "dynamodb"


class TestElasticLoadBalancing:
    def test_create_load_balancer_alb(self):
        with open(
            "test/services/samples/elasticloadbalancing_CreateLoadBalancer_alb.json"
        ) as f:
            data = json.loads(f.read())

        result = build_result(data)

        assert result["resource_id"] == ["test-alb"]
        assert result["identity"] == "user/test"
        assert result["region"] == "ap-northeast-2"
        assert result["event_name"] == "CreateLoadBalancer"
        assert result["source_ip_address"] == "127.0.0.1"
        assert result["event_source"] == "elasticloadbalancing"

    def test_create_load_balancer_clb(self):
        with open(
            "test/services/samples/elasticloadbalancing_CreateLoadBalancer_clb.json"
        ) as f:
            data = json.loads(f.read())

        result = build_result(data)

        assert result["resource_id"] == ["test-clb"]
        assert result["identity"] == "user/test"
        assert result["region"] == "ap-northeast-2"
        assert result["event_name"] == "CreateLoadBalancer"
        assert result["source_ip_address"] == "127.0.0.1"
        assert result["event_source"] == "elasticloadbalancing"


class TestCloudFront:
    def test_create_distribution(self):
        with open("test/services/samples/cloudfront_CreateDistribution.json") as f:
            data = json.loads(f.read())

        result = build_result(data)

        assert result["resource_id"] == ["DISTRIBUTION_ID"]
        assert result["identity"] == "user/test"
        assert result["region"] == "us-east-1"
        assert result["event_name"] == "CreateDistribution"
        assert result["source_ip_address"] == "127.0.0.1"
        assert result["event_source"] == "cloudfront"


class TestECR:
    def test_create_repository(self):
        with open("test/services/samples/ecr_CreateRepository.json") as f:
            data = json.loads(f.read())

        result = build_result(data)

        assert result["resource_id"] == ["test"]
        assert result["identity"] == "user/test_user"
        assert result["region"] == "ap-northeast-2"
        assert result["event_name"] == "CreateRepository"
        assert result["source_ip_address"] == "127.0.0.1"
        assert result["event_source"] == "ecr"


class TestSQS:
    def test_create_queue(self):
        with open("test/services/samples/sqs_CreateQueue.json") as f:
            data = json.loads(f.read())

        result = build_result(data)

        assert result["resource_id"] == ["test-queue"]
        assert result["identity"] == "user/test_user"
        assert result["region"] == "ap-northeast-2"
        assert result["event_name"] == "CreateQueue"
        assert result["source_ip_address"] == "127.0.0.1"
        assert result["event_source"] == "sqs"


class TestSNS:
    def test_create_topic(self):
        with open("test/services/samples/sns_CreateTopic.json") as f:
            data = json.loads(f.read())

        result = build_result(data)

        assert result["resource_id"] == ["sns-test.fifo"]
        assert result["identity"] == "user/test_user"
        assert result["region"] == "ap-northeast-2"
        assert result["event_name"] == "CreateTopic"
        assert result["source_ip_address"] == "127.0.0.1"
        assert result["event_source"] == "sns"
