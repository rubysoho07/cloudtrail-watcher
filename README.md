# CloudTrail Watcher

When a resource like EC2, S3, and Lambda was created...

* You can be notified via email or Slack message by using Amazon SNS. 
* You can set default tags for resources.

## Deploy Infrastructures

### Deploy with SAM (Serverless Application Model)

```shell
$ cd deploy/sam
$ ACCOUNT_ID=$(aws sts get-caller-identity | jq -r '.Account')
$ sam build
$ sam deploy --parameter-overrides ResourcesDefaultPrefix=cloudtrailwatcher-$ACCOUNT_ID \ 
             --capabilities CAPABILITY_NAMED_IAM

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
```