# cloudtrail-watcher
Watching AWS CloudTrail Tool


## Deploy

### Deploy with SAM (Serverless Application Model)

```shell
$ cd deploy/sam
$ ACCOUNT_ID=$(aws sts get-caller-identity | jq -r '.Account')
$ sam build
$ sam deploy --parameter-overrides ResourcesDefaultPrefix=cloudtrailwatcher-$ACCOUNT_ID --capabilities CAPABILITY_NAMED_IAM
```