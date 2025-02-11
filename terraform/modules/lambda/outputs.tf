output "s3_upload_completed_lambda_arn" {
  description = "ARN of the deployed Lambda function"
  value       = aws_lambda_function.s3_upload_completed_lambda.arn
}