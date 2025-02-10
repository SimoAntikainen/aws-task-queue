terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.84"
    }
  }
}

provider "aws" {
  region = var.region
}

module "dynamodb" {
  source      = "../../modules/dynamodb"
  tags = {
    Environment = var.environment
    Project     = var.project
  }
}

module "s3" {
  source      = "../../modules/s3"
  bucket_name = var.task_bucket_name
  #lambda_function_arn = module.lambda.s3_upload_completed_lambda_arn
  tags = {
    Environment = var.environment
    Project     = var.project
  }
  
}

data "aws_caller_identity" "current" {}

module "lambda" {
  source      = "../../modules/lambda"
  account_id = data.aws_caller_identity.current.account_id
  s3_bucket_arn = module.s3.bucket_arn
  s3_bucket_name =  module.s3.bucket_name
  sqs_results_queue_arn = module.sqs.sqs_queue_arn
  sqs_results_queue_url = module.sqs.sqs_queue_url

  environment =  var.environment
  project = var.project
  tags = {
    Environment = var.environment
    Project     = var.project
  }
}


module "sqs" {
  source = "../../modules/sqs"

  tags = {
    Environment = var.environment
    Project     = var.project
  }
}


