variable "aws_region" {
  type = string
  default = "us-east-1"
  description = "AWS Region to deploy CloudTrail Watcher"
}

variable "aws_profile" {
  type = string
  default = "default"
  description = "AWS Profile to deploy CloudTrail Watcher"
}

variable "resource_prefix" {
  type = string
  description = "Prefix for resources related with CloudTrail Watcher"

  validation {
    condition = can(regex("^(|[a-z0-9\\-]+)$", var.resource_prefix))
    error_message = "Default prefix for resources MUST be blank or contain lowercase letters, hyphens, numbers."
  }
}