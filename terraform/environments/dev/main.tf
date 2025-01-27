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
  tags = {
    Environment = var.environment
    Project     = var.project
  }
}

module "lambda" {
  source      = "../../modules/lambda"
  tags = {
    Environment = var.environment
    Project     = var.project
  }
}