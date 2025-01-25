variable "region" {
  description = "AWS region"
  type        = string
  default     = "eu-west-1"
}

variable "task_bucket_name" {
  description = "Task bucket name"
  type        = string
  default     = "dev-task-bucket"
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