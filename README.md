# CloudTrail Watcher

English Version: [README.en.md](./README.en.md)

EC2, S3, Lambda 함수와 같은 AWS 리소스를 생성할 때,

* 슬랙 메시지(Incoming Webhook)나 이메일(Amazon SNS 사용)으로 알림을 받을 수 있습니다. 
* CloudTrail Watcher Lambda 함수가 `User` 태그를 자동으로 AWS 리소스에 추가합니다.

## 아키텍처

![Architecture](./cloudtrail-watcher-architecture.png)

## 지원하는 AWS 리소스와 활동

* 콘솔 로그인
* IAM (User, Group, Role, Policy, Instance Profile)
* EC2 (Instance, Security Group)
* RDS (Cluster, Instance)
* S3 (Bucket)
* ElastiCache (Redis, Memcached)
* EMR (Cluster)
* Lambda (Function)
* Redshift (Cluster)
* ECS (Cluster)
* EKS (Cluster)
* DocumentDB (Cluster, Instance)
* MSK(Managed Streaming for Apache Kafka) (Cluster)
* MWAA(Managed Workflow for Apache Airflow) (Environment)
* DynamoDB (Table)
* 🆕 ELB (CLB, ALB, NLB, GLB)
* 🆕 CloudFront (Distribution)

## 인프라 구축

### SAM (Serverless Application Model)으로 인프라 구성하기

```shell
$ cd deploy/sam
$ ACCOUNT_ID=$(aws sts get-caller-identity | jq -r '.Account')
$ sam build
$ sam deploy --stack-name cloudtrail-watcher \
             --parameter-overrides ResourcesDefaultPrefix=cloudtrailwatcher-$ACCOUNT_ID \ 
             --capabilities CAPABILITY_NAMED_IAM
             --tags 'User=cloudtrail-watcher'
             
# 배포 시 추가 파라미터를 오버라이드 하고 싶다면
$ sam deploy --stack-name cloudtrail-watcher \
             --parameter-overrides ResourcesDefaultPrefix=your_prefix SetMandatoryTag=true \
             --capabilities CAPABILITY_NAMED_IAM
             # If you want more tags
             --tags 'User=cloudtrail-watcher' 'Team=DevOps' 
             
# SAM stack 배포
$ sam delete 
```

SAM CLI에 익숙하지 않으시다면, 아래 명령을 사용하시기를 권장합니다. 

```shell
$ cd deploy/sam
$ sam build
$ sam deploy --guided
```

### Terraform으로 인프라 구성하기 

```shell
$ cd deploy/terraform
$ terraform init

# 생성하는 리소스에 접두어를 붙이고 싶다면
$ terraform apply -var 'aws_region=ap-northeast-2' -var 'resource_prefix=<your_resource_prefix>'

# 생성하는 리소스에 접두어를 붙이고 싶지 않다면
$ terraform apply -var 'aws_region=ap-northeast-2' -var 'resource_prefix='

# 배포된 인프라 삭제하기
$ terraform destroy -var 'aws_region=ap-northeast-2' \
                    -var 'resource_prefix=<your_resource_prefix or blank>'
                    # 더 많은 변수를 추가하는 경우
                    -var 'variable_name=value'
```

## 알림 받기

### Slack

* 함수의 `SLACK_WEBHOOK_URL` 환경 변수를 Slack의 Incoming Webhook URL로 변경합니다. 
* 기본값은 `DISABLED` 입니다. 리소스 생성 알림을 슬랙으로 받고 싶지 않다면, 이 환경 변수를 `DISABLED`로 지정해 주세요.

#### SAM

SAM CLI로 배포한다면, 아래와 같이 `--parameter-overrides` 옵션을 추가해 주세요.

```shell
sam deploy --parameter-overrides SlackWebhookURL=https://hooks.slack.com/services/...
```

#### Terraform

`terraform apply` 명령을 실행할 때, 옵션을 추가합니다.

```shell
terraform apply -var 'slack_webhook_url=https://hooks.slack.com/services/...'
```

### 이메일

```shell
# SNS Topic ARN을 가져 옵니다. 
TOPIC_ARN=$(aws sns list-topics | jq -r '.Topics[].TopicArn' | grep cloudtrailwatcher)

# SNS Topic 구독하기
aws sns subscribe --topic-arn $TOPIC_ARN \ 
                  --protocol email \ 
                  --notification-endpoint your@email.address
```

AWS SNS로부터 이메일을 수신했다면, 구독을 완료하기 위해 이메일을 확인하세요.

## 필수 태그 지정하기

CloudTrail Watcher는 새로 생성한 리소스에 대해 태그 추가를 지원합니다. Lambda 함수가 리소스에 `User` 태그가 있는지 확인합니다. 
함수가 `User` 태그를 찾을 수 없으면, 여러분을 대신해서 `User` 태그를 추가해 줍니다. 

태그 추가는 슬랙 메시지나 Amazon SNS를 통해 이메일을 보내는 데 영향을 주지 않습니다.  

### 사용법

* Lambda 함수에 `SET_MANDATORY_TAG` 환경 변수를 추가합니다. 환경 변수 값이 `DISABLED`, `0`, `False`, `false`가 아니면, 필수 태그 추가 기능이 동작합니다.

#### SAM

SAM CLI로 배포할 때, `--parameter-overrides SetMandatoryTag=true` 옵션을 아래와 같이 추가합니다.

```shell
sam deploy --parameter-overrides ResourcesDefaultPrefix=cloudtrailwatcher-$ACCOUNT_ID \ 
                                 SetMandatoryTag=true
```

#### Terraform

`terraform apply` 명령을 실행할 때, `-var 'set_mandatory_tag=true'` 옵션을 추가합니다.

```shell
terraform apply -var 'aws_region=ap-northeast-2' \
                -var 'resource_prefix=<your_resource_prefix or blank>' \
                -var 'set_mandatory_tag=true'
```

## 참고자료

* [CloudTrail Log Event Reference](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-event-reference.html)