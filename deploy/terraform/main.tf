terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = ">= 2.0.0"
    }
  }
}

provider "aws" {
  profile = var.aws_profile
  region = var.aws_region
}

data "aws_caller_identity" "current_account" {}

data "archive_file" "watcher_function_codes" {
  type = "zip"
  source_dir = "../../functions/watcher/"
  output_path = "/tmp/cloudtrailwatcher_function.zip"
}

locals {
  resource_prefix = var.resource_prefix == "" ? "cloudtrailwatcher-${data.aws_caller_identity.current_account.account_id}" : var.resource_prefix
}

resource "aws_lambda_function" "watcher_function" {
  function_name = local.resource_prefix
  description = "CloudTrail Watcher Funcion"
  role = aws_iam_role.watcher_function_role.arn
  filename = data.archive_file.watcher_function_codes.output_path
  timeout = 120
  memory_size = 512
  runtime = "python3.9"
  handler = "lambda_function.handler"
  environment {
    variables = {
      SNS_TOPIC_ARN = aws_sns_topic.watcher_sns_topic.arn
    }
  }
}

resource "aws_lambda_permission" "watcher_function_permission" {
  action = "lambda:InvokeFunction"
  function_name = aws_lambda_function.watcher_function.function_name
  principal = "s3.amazonaws.com"
}

resource "aws_s3_bucket" "watcher_logs_bucket" {
  bucket = local.resource_prefix
}

resource "aws_s3_bucket_notification" "watcher_logs_bucket_notification" {
  bucket = aws_s3_bucket.watcher_logs_bucket.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.watcher_function.arn
    events = ["s3:ObjectCreated:*"]
  }

  depends_on = [aws_lambda_permission.watcher_function_permission]
}

resource "aws_s3_bucket_lifecycle_configuration" "watcher_logs_bucket_lifecycle" {
  bucket = aws_s3_bucket.watcher_logs_bucket.id

  rule {
    id = "DeleteLogAfter1Year"
    status = "Enabled"
    expiration {
      days = 365
    }
  }
}

resource "aws_s3_bucket_policy" "watcher_logs_bucket_policy" {
  bucket = aws_s3_bucket.watcher_logs_bucket.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "cloudtrail.amazonaws.com"
        }
        Action = "s3:GetBucketAcl"
        Resource = aws_s3_bucket.watcher_logs_bucket.arn
      },{
        Effect = "Allow"
        Principal = {
          Service = "cloudtrail.amazonaws.com"
        }
        Action = "s3:PutObject"
        Resource = "${aws_s3_bucket.watcher_logs_bucket.arn}/*"
      }
    ]
  })
}

resource "aws_cloudtrail" "watcher_trail" {
  depends_on = [aws_s3_bucket_policy.watcher_logs_bucket_policy]

  name = local.resource_prefix
  s3_bucket_name = aws_s3_bucket.watcher_logs_bucket.id
  enable_logging = true
}

resource "aws_sns_topic" "watcher_sns_topic" {
  name = local.resource_prefix
}

resource "aws_iam_role" "watcher_function_role" {
  name = "${local.resource_prefix}-role"
  description = "Role for CloudTrail Watcher Lambda function"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      },
    ]
  })

  inline_policy {
    name = "${local.resource_prefix}-policy"
    policy = jsonencode({
      Version = "2012-10-17"
      Statement = [
        {
          Effect = "Allow"
          Action = "s3:GetObject"
          Resource = "${aws_s3_bucket.watcher_logs_bucket.arn}/*"
        },{
          Effect = "Allow"
          Action = "sns:Publish"
          Resource = aws_sns_topic.watcher_sns_topic.arn
        }
      ]
    })
  }
}
