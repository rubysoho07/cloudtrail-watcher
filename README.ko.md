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
* EC2 (Instance, Security Group (보안그룹 생성, 규칙 추가/수정/삭제))
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
* ELB (CLB, ALB, NLB, GLB)
* CloudFront (Distribution)
* ECR (Repository)
* SNS (Topic)
* SQS (Queue)

## 인프라 구축

이 애플리케이션은 Lambda Layer와 IAM Policy를 포함합니다. 아래와 같은 방법으로 배포할 수 있습니다. 

### SAM (Serverless Application Model) 으로 배포하기

추가 리소스를 SAM으로 배포할 수 있습니다. `deploy/sam/template-with-layer.yaml` 파일을 기준으로 배포해 주세요. 

SAM과 CloudFormation의 제약 사항으로 인해, 새로운 CloudTrail과 S3 버킷을 생성하는 경우에만 배포 가능하니 참고해 주세요. 

### 배포 옵션 (SAM 템플릿 파라미터)

| 이름 | 설명 | 타입 | 기본값 | 필수 여부 |
|------|-------------|------|---------|----------|
| ResourcesDefaultPrefix | CloudTrail Watcher와 관련된 리소스의 접두사 (미설정 시 'cloudtrailwatcher-<YOUR_ACCOUNT_ID>') | string | "" | no |
| SlackWebhookURL | Slack 웹훅의 URL (비활성화 필요 시 "DISABLED"로 설정) | string | "DISABLED" | no |
| SetMandatoryTag | 리소스가 생성될 때마다 'User' 태그를 추가합니다. 이 기능을 활성화 하려면, 이 파라미터를 "True"로 설정하세요. | string | "False" | no |
| DisableAutoscalingAlarm | 오토 스케일링으로 생성한 리소스에 대한 알림을 보내지 않습니다. 이 기능을 활성화 하려면, 이 파라미터를 "True"로 설정하세요. | string | "False" | no |

### Terraform으로 배포하기

추가 리소스를 Terraform으로 배포할 수 있습니다. Terraform 모듈 관련 페이지를 참고하세요: [terraform-aws-cloudtrail-watcher](https://github.com/rubysoho07/terraform-aws-cloudtrail-watcher)

## 참고자료

* [CloudTrail Log Event Reference](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-event-reference.html)