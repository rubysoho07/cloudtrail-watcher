# CloudTrail Watcher

When a resource like EC2, S3, and Lambda was created...

* You can be notified via email or Slack message by using Amazon SNS. 
* You can set default tags for resources.

## Supported AWS Resources & Actions

* EC2 (Instance, Security Group)
* RDS (Cluster, Instance)
* S3 (Bucket)
* ElastiCache (Redis, Memcached)
* EMR (Cluster)
* Lambda (Function)
* Redshift (Cluster)
* ECS (Cluster)
* EKS (Cluster)
* IAM (User, Group, Role, Policy, Instance Profile)
* Console Login

## Deploy Infrastructures

### Deploy with SAM (Serverless Application Model)

```shell
$ cd deploy/sam
$ ACCOUNT_ID=$(aws sts get-caller-identity | jq -r '.Account')
$ sam build
$ sam deploy --stack-name cloudtrail-watcher \
             --parameter-overrides ResourcesDefaultPrefix=cloudtrailwatcher-$ACCOUNT_ID \ 
             --capabilities CAPABILITY_NAMED_IAM
             --tags 'User=cloudtrail-watcher'
             
# If you want to override additional parameters when deploying
$ sam deploy --stack-name cloudtrail-watcher \
             --parameter-overrides ResourcesDefaultPrefix=cloudtrailwatcher-$ACCOUNT_ID SetMandatoryTag=true \
             --capabilities CAPABILITY_NAMED_IAM
             # If you want more tags
             --tags 'User=cloudtrail-watcher' 'Team=DevOps' 
             
# Destroy SAM stack
$ sam delete 
```

### Deploy with Terraform 

```shell
$ cd deploy/terraform
$ terraform init

# If you want to set prefix for resources
$ terraform apply -var 'aws_region=ap-northeast-2' -var 'resource_prefix=<your_resource_prefix>'

# If you don't need to set prefix for resources
$ terraform apply -var 'aws_region=ap-northeast-2' -var 'resource_prefix='

# Destroy infrastructure deployments
$ terraform destroy -var 'aws_region=ap-northeast-2' \
                    -var 'resource_prefix=<your_resource_prefix or blank>'
                    # If you have to set more variables...
                    -var 'variable_name=value'
```

## Notification

### Slack

* Change function's `SLACK_WEBHOOK_URL` environment variable to Slack Incoming Webhook URL. 
* Default value is `DISABLED`. If you don't want to notify resource creation via Slack, set this variable `DISABLED`.

#### SAM

When you deploy with SAM CLI, add `--parameter-overrides` option like below:

```shell
sam deploy --parameter-overrides SlackWebhookURL=https://hooks.slack.com/services/...
```

#### Terraform

When you run `terraform apply` command, add option:

```shell
terraform apply -var 'slack_webhook_url=https://hooks.slack.com/services/...'
```

### Email

```shell
# Get SNS Topic ARN
TOPIC_ARN=$(aws sns list-topics | jq -r '.Topics[].TopicArn' | grep cloudtrailwatcher)

# Subscribe
aws sns subscribe --topic-arn $TOPIC_ARN --protocol email --notification-endpoint your@email.address
```

If you receive email from AWS SNS, please confirm the email to complete subscription.

## Set Mandatory Tag

CloudTrail Watcher supports create tags for newly created resources. Lambda function checks `User` tag exists on these resources. 
If the function cannot find `User` tag on them, it creates `User` tag on behalf of you. 

Creating tag doesn't influence sending messages via Slack or Email by using Amazon SNS. 

### Instruction

* Set `SET_MANDATORY_TAG` environment variable on Lambda function: If the value is not in `DISABLED`, `0`, `False`, `false`, the feature setting mandatory tags will work.

#### SAM

When you deploy with SAM CLI, add `--parameter-overrides SetMandatoryTag=true` option like below:

```shell
sam deploy --parameter-overrides ResourcesDefaultPrefix=cloudtrailwatcher-$ACCOUNT_ID \ 
                                 SetMandatoryTag=true
```

#### Terraform

When you run `terraform apply` command, add `-var 'set_mandatory_tag=true'`option:

```shell
terraform apply -var 'aws_region=ap-northeast-2' \
                -var 'resource_prefix=<your_resource_prefix or blank>' \
                -var 'set_mandatory_tag=true'
```

## References

* [CloudTrail Log Event Reference](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-event-reference.html)