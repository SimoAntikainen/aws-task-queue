output "my_lambda_arn" {
  description = "ARN of the deployed Lambda function"
  value       = aws_lambda_function.my_lambda.arn
}