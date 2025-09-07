import json
import unittest

from cloudtrail_watcher.utils import build_result


class EC2Test(unittest.TestCase):

    def test_create_security_group(self):
        with open('./samples/ec2_CreateSecurityGroup.json') as f:
            data = json.loads(f.read())

        result = build_result(data)

        self.assertEqual(result['resource_id'], ['sg-YOUR_SECURITY_GROUP_ID'])
        self.assertEqual(result['identity'], 'user/test')
        self.assertEqual(result['region'], 'ap-northeast-2')
        self.assertEqual(result['event_name'], 'CreateSecurityGroup')
        self.assertEqual(result['source_ip_address'], '172.0.0.1')
        self.assertEqual(result['event_source'], 'ec2')

    def test_run_instances_single(self):
        with open('./samples/ec2_RunInstances_single.json') as f:
            data = json.loads(f.read())

        result = build_result(data)

        self.assertEqual(result['resource_id'], ['i-YOUR_INSTANCE_IDS'])
        self.assertEqual(result['identity'], 'user/test')
        self.assertEqual(result['region'], 'ap-northeast-2')
        self.assertEqual(result['event_name'], 'RunInstances')
        self.assertEqual(result['source_ip_address'], '172.0.0.1')
        self.assertEqual(result['event_source'], 'ec2')

    def test_run_instances_multi(self):
        with open('./samples/ec2_RunInstances_multi.json') as f:
            data = json.loads(f.read())

        result = build_result(data)

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

        result = build_result(data)

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

        result = build_result(data)

        self.assertEqual(result['resource_id'], ['cloudtrailwatcher-000000000000'])
        self.assertEqual(result['identity'], 'user/test')
        self.assertEqual(result['region'], 'ap-northeast-2')
        self.assertEqual(result['event_name'], 'CreateBucket')
        self.assertEqual(result['source_ip_address'], '172.0.0.1')
        self.assertEqual(result['event_source'], 's3')


class RDSTest(unittest.TestCase):
    def test_create_db_cluster(self):
        with open('./samples/rds_CreateDBCluster.json') as f:
            data = json.loads(f.read())

        result = build_result(data)

        self.assertEqual(result['resource_id'], ['test-db'])
        self.assertEqual(result['identity'], 'user/test')
        self.assertEqual(result['region'], 'ap-northeast-2')
        self.assertEqual(result['event_name'], 'CreateDBCluster')
        self.assertEqual(result['source_ip_address'], 'AWS Internal')
        self.assertEqual(result['event_source'], 'rds')

    def test_create_db_instance(self):
        with open('./samples/rds_CreateDBInstance.json') as f:
            data = json.loads(f.read())

        result = build_result(data)

        self.assertEqual(result['resource_id'], ['test-db-instance-1'])
        self.assertEqual(result['identity'], 'user/test')
        self.assertEqual(result['region'], 'ap-northeast-2')
        self.assertEqual(result['event_name'], 'CreateDBInstance')
        self.assertEqual(result['source_ip_address'], 'AWS Internal')
        self.assertEqual(result['event_source'], 'rds')

    def test_create_db_cluster_docdb(self):
        with open('./samples/rds_CreateDBCluster_DocDB.json') as f:
            data = json.loads(f.read())

        result = build_result(data)

        self.assertEqual(result['resource_id'], ['ctw-test'])
        self.assertEqual(result['identity'], 'user/test_user')
        self.assertEqual(result['region'], 'ap-northeast-2')
        self.assertEqual(result['event_name'], 'CreateDBCluster')
        self.assertEqual(result['source_ip_address'], '127.0.0.1')
        self.assertEqual(result['event_source'], 'documentdb')

    def test_create_db_instance_docdb(self):
        with open('./samples/rds_CreateDBInstance_DocDB.json') as f:
            data = json.loads(f.read())

        result = build_result(data)

        self.assertEqual(result['resource_id'], ['ctw-test'])
        self.assertEqual(result['identity'], 'user/test_user')
        self.assertEqual(result['region'], 'ap-northeast-2')
        self.assertEqual(result['event_name'], 'CreateDBInstance')
        self.assertEqual(result['source_ip_address'], '127.0.0.1')
        self.assertEqual(result['event_source'], 'documentdb')


class ElastiCacheTest(unittest.TestCase):
    def test_create_cache_cluster(self):
        with open('./samples/elasticache_CreateCacheCluster.json') as f:
            data = json.loads(f.read())

        result = build_result(data)

        self.assertEqual(result['resource_id'], ['test-memcached'])
        self.assertEqual(result['identity'], 'user/test')
        self.assertEqual(result['region'], 'ap-northeast-2')
        self.assertEqual(result['event_name'], 'CreateCacheCluster')
        self.assertEqual(result['source_ip_address'], 'AWS Internal')
        self.assertEqual(result['event_source'], 'elasticache')

    def test_create_replication_group(self):
        with open('./samples/elasticache_CreateReplicationGroup.json') as f:
            data = json.loads(f.read())

        result = build_result(data)

        self.assertEqual(result['resource_id'], ['test'])
        self.assertEqual(result['identity'], 'user/test')
        self.assertEqual(result['region'], 'ap-northeast-2')
        self.assertEqual(result['event_name'], 'CreateReplicationGroup')
        self.assertEqual(result['source_ip_address'], 'AWS Internal')
        self.assertEqual(result['event_source'], 'elasticache')


class EMRTest(unittest.TestCase):
    def test_run_job_flow(self):
        with open('./samples/elasticmapreduce_RunJobFlow.json') as f:
            data = json.loads(f.read())

        result = build_result(data)

        self.assertEqual(result['resource_id'], ['j-2E1G6JJE6X1MQ'])
        self.assertEqual(result['identity'], 'user/test')
        self.assertEqual(result['region'], 'ap-northeast-2')
        self.assertEqual(result['event_name'], 'RunJobFlow')
        self.assertEqual(result['source_ip_address'], 'AWS Internal')
        self.assertEqual(result['event_source'], 'elasticmapreduce')


class RedshiftTest(unittest.TestCase):
    def test_create_cluster(self):
        with open('./samples/redshift_CreateCluster.json') as f:
            data = json.loads(f.read())

        result = build_result(data)

        self.assertEqual(result['resource_id'], ['test-goni'])
        self.assertEqual(result['identity'], 'user/test')
        self.assertEqual(result['region'], 'ap-northeast-2')
        self.assertEqual(result['event_name'], 'CreateCluster')
        self.assertEqual(result['source_ip_address'], 'AWS Internal')
        self.assertEqual(result['event_source'], 'redshift')


class ECSTest(unittest.TestCase):
    def test_create_cluster(self):
        with open('./samples/ecs_CreateCluster.json') as f:
            data = json.loads(f.read())

        result = build_result(data)

        self.assertEqual(result['resource_id'], ['test-ecs'])
        self.assertEqual(result['identity'], 'user/test')
        self.assertEqual(result['region'], 'ap-northeast-2')
        self.assertEqual(result['event_name'], 'CreateCluster')
        self.assertEqual(result['source_ip_address'], 'cloudformation.amazonaws.com')
        self.assertEqual(result['event_source'], 'ecs')


class EKSTest(unittest.TestCase):
    def test_create_cluster(self):
        with open('./samples/eks_CreateCluster.json') as f:
            data = json.loads(f.read())

        result = build_result(data)

        self.assertEqual(result['resource_id'], ['test'])
        self.assertEqual(result['identity'], 'user/test')
        self.assertEqual(result['region'], 'ap-northeast-2')
        self.assertEqual(result['event_name'], 'CreateCluster')
        self.assertEqual(result['source_ip_address'], '172.0.0.1')
        self.assertEqual(result['event_source'], 'eks')


class IAMTest(unittest.TestCase):
    def test_create_user(self):
        with open('./samples/iam_CreateUser.json') as f:
            data = json.loads(f.read())

        result = build_result(data)

        self.assertEqual(result['resource_id'], ['test_user'])
        self.assertEqual(result['identity'], 'user/test')
        self.assertEqual(result['region'], 'us-east-1')
        self.assertEqual(result['event_name'], 'CreateUser')
        self.assertEqual(result['source_ip_address'], 'AWS Internal')
        self.assertEqual(result['event_source'], 'iam')

    def test_create_group(self):
        with open('./samples/iam_CreateGroup.json') as f:
            data = json.loads(f.read())

        result = build_result(data)

        self.assertEqual(result['resource_id'], ['test_group'])
        self.assertEqual(result['identity'], 'user/test')
        self.assertEqual(result['region'], 'us-east-1')
        self.assertEqual(result['event_name'], 'CreateGroup')
        self.assertEqual(result['source_ip_address'], 'AWS Internal')
        self.assertEqual(result['event_source'], 'iam')

    def test_create_policy(self):
        with open('./samples/iam_CreatePolicy.json') as f:
            data = json.loads(f.read())

        result = build_result(data)

        self.assertEqual(result['resource_id'], ['your_policy_name'])
        self.assertEqual(result['identity'], 'user/test')
        self.assertEqual(result['region'], 'us-east-1')
        self.assertEqual(result['event_name'], 'CreatePolicy')
        self.assertEqual(result['source_ip_address'], '172.0.0.1')
        self.assertEqual(result['event_source'], 'iam')

    def test_create_role(self):
        with open('./samples/iam_CreateRole.json') as f:
            data = json.loads(f.read())

        result = build_result(data)

        self.assertEqual(result['resource_id'], ['role/service-role/your_role_name'])
        self.assertEqual(result['identity'], 'user/test')
        self.assertEqual(result['region'], 'us-east-1')
        self.assertEqual(result['event_name'], 'CreateRole')
        self.assertEqual(result['source_ip_address'], '172.0.0.1')
        self.assertEqual(result['event_source'], 'iam')

    def test_create_policy_version(self):
        with open('./samples/iam_CreatePolicyVersion.json') as f:
            data = json.loads(f.read())

        result = build_result(data)

        self.assertEqual(result['resource_id'], ['test-policy:v2'])
        self.assertEqual(result['identity'], 'user/test')
        self.assertEqual(result['region'], 'us-east-1')
        self.assertEqual(result['event_name'], 'CreatePolicyVersion')
        self.assertEqual(result['source_ip_address'], 'AWS Internal')
        self.assertEqual(result['event_source'], 'iam')

    def test_create_instance_profile(self):
        with open('./samples/iam_CreateInstanceProfile.json') as f:
            data = json.loads(f.read())

        result = build_result(data)

        self.assertEqual(result['resource_id'], ['EC2_Role'])
        self.assertEqual(result['identity'], 'user/test')
        self.assertEqual(result['region'], 'us-east-1')
        self.assertEqual(result['event_name'], 'CreateInstanceProfile')
        self.assertEqual(result['source_ip_address'], 'AWS Internal')
        self.assertEqual(result['event_source'], 'iam')


class OpenSearchTest(unittest.TestCase):
    def test_create_db_cluster(self):
        with open('./samples/es_CreateDomain.json') as f:
            data = json.loads(f.read())

        result = build_result(data)

        self.assertEqual(result['resource_id'], ['test-es2'])
        self.assertEqual(result['identity'], 'user/test')
        self.assertEqual(result['region'], 'ap-northeast-2')
        self.assertEqual(result['event_name'], 'CreateDomain')
        self.assertEqual(result['source_ip_address'], 'AWS Internal')
        self.assertEqual(result['event_source'], 'es')


class MSKTest(unittest.TestCase):
    def test_create_cluster_v2(self):
        with open('./samples/kafka_CreateClusterV2.json') as f:
            data = json.loads(f.read())

        result = build_result(data)

        self.assertEqual(result['resource_id'], ['ct-watcher-test'])
        self.assertEqual(result['identity'], 'user/test_user')
        self.assertEqual(result['region'], 'ap-northeast-2')
        self.assertEqual(result['event_name'], 'CreateClusterV2')
        self.assertEqual(result['source_ip_address'], '172.0.0.1')
        self.assertEqual(result['event_source'], 'kafka')


class MWAATest(unittest.TestCase):
    def test_create_environment(self):
        with open('./samples/airflow_CreateEnvironment.json') as f:
            data = json.loads(f.read())

        result = build_result(data)

        self.assertEqual(result['resource_id'], ['ct-watcher-test'])
        self.assertEqual(result['identity'], 'user/test_user')
        self.assertEqual(result['region'], 'ap-northeast-2')
        self.assertEqual(result['event_name'], 'CreateEnvironment')
        self.assertEqual(result['source_ip_address'], '172.0.0.1')
        self.assertEqual(result['event_source'], 'airflow')


class DynamoDBTest(unittest.TestCase):
    def test_create_table(self):
        with open('./samples/dynamodb_CreateTable.json') as f:
            data = json.loads(f.read())

        result = build_result(data)

        self.assertEqual(result['resource_id'], ['ct-watcher-test'])
        self.assertEqual(result['identity'], 'user/test_user')
        self.assertEqual(result['region'], 'ap-northeast-2')
        self.assertEqual(result['event_name'], 'CreateTable')
        self.assertEqual(result['source_ip_address'], '172.0.0.1')
        self.assertEqual(result['event_source'], 'dynamodb')


class ElasticLoadBalancingTest(unittest.TestCase):
    def test_create_load_balancer_alb(self):
        with open('./samples/elasticloadbalancing_CreateLoadBalancer_alb.json') as f:
            data = json.loads(f.read())

        result = build_result(data)

        self.assertEqual(result['resource_id'], ['test-alb'])
        self.assertEqual(result['identity'], 'user/test')
        self.assertEqual(result['region'], 'ap-northeast-2')
        self.assertEqual(result['event_name'], 'CreateLoadBalancer')
        self.assertEqual(result['source_ip_address'], '127.0.0.1')
        self.assertEqual(result['event_source'], 'elasticloadbalancing')

    def test_create_load_balancer_clb(self):
        with open('./samples/elasticloadbalancing_CreateLoadBalancer_clb.json') as f:
            data = json.loads(f.read())

        result = build_result(data)

        self.assertEqual(result['resource_id'], ['test-clb'])
        self.assertEqual(result['identity'], 'user/test')
        self.assertEqual(result['region'], 'ap-northeast-2')
        self.assertEqual(result['event_name'], 'CreateLoadBalancer')
        self.assertEqual(result['source_ip_address'], '127.0.0.1')
        self.assertEqual(result['event_source'], 'elasticloadbalancing')


class CloudFrontTest(unittest.TestCase):
    def test_create_distribution(self):
        with open('./samples/cloudfront_CreateDistribution.json') as f:
            data = json.loads(f.read())

        result = build_result(data)

        self.assertEqual(result['resource_id'], ['DISTRIBUTION_ID'])
        self.assertEqual(result['identity'], 'user/test')
        self.assertEqual(result['region'], 'us-east-1')
        self.assertEqual(result['event_name'], 'CreateDistribution')
        self.assertEqual(result['source_ip_address'], '127.0.0.1')
        self.assertEqual(result['event_source'], 'cloudfront')


class ECRTest(unittest.TestCase):
    def test_create_repository(self):
        with open('./samples/ecr_CreateRepository.json') as f:
            data = json.loads(f.read())

        result = build_result(data)

        self.assertEqual(result['resource_id'], ['test'])
        self.assertEqual(result['identity'], 'user/test_user')
        self.assertEqual(result['region'], 'ap-northeast-2')
        self.assertEqual(result['event_name'], 'CreateRepository')
        self.assertEqual(result['source_ip_address'], '127.0.0.1')
        self.assertEqual(result['event_source'], 'ecr')


class SQSTest(unittest.TestCase):
    def test_create_queue(self):
        with open('./samples/sqs_CreateQueue.json') as f:
            data = json.loads(f.read())

        result = build_result(data)

        self.assertEqual(result['resource_id'], ['test-queue'])
        self.assertEqual(result['identity'], 'user/test_user')
        self.assertEqual(result['region'], 'ap-northeast-2')
        self.assertEqual(result['event_name'], 'CreateQueue')
        self.assertEqual(result['source_ip_address'], '127.0.0.1')
        self.assertEqual(result['event_source'], 'sqs')


class SNSTest(unittest.TestCase):
    def test_create_topic(self):
        with open('./samples/sns_CreateTopic.json') as f:
            data = json.loads(f.read())

        result = build_result(data)

        self.assertEqual(result['resource_id'], ['sns-test.fifo'])
        self.assertEqual(result['identity'], 'user/test_user')
        self.assertEqual(result['region'], 'ap-northeast-2')
        self.assertEqual(result['event_name'], 'CreateTopic')
        self.assertEqual(result['source_ip_address'], '127.0.0.1')
        self.assertEqual(result['event_source'], 'sns')