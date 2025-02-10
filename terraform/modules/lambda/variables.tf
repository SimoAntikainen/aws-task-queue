variable "tags" {
  description = "Tags to apply to the Lambdas"
  type        = map(string)
}

variable "region" {
  description = "AWS region"
  type        = string
  default     = "eu-west-1"
}

variable "account_id" {
  description = "The AWS account ID."
  type        = string
}

variable "s3_bucket_name" {
  description = "The name of the S3 bucket that will trigger this Lambda function"
  type        = string
}

variable "s3_bucket_arn" {
  description = "ARN of the S3 bucket that will trigger this Lambda function on eg. on upload"
  type        = string
}

variable "sqs_results_queue_arn" {
  description = "The name of the SQS queue that lambda calls"
  type        = string

}
variable "sqs_results_queue_url" {
  description = "ARN of the SQS queue that lambda calls" 
  type        = string

}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "Development"
}

variable "project" {
  description = "Project name"
  type        = string
  default     = "AIDetectionApp"
}
