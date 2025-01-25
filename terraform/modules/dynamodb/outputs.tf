output "process_state_table_name" {
  description = "The name of the Process State DynamoDB table"
  value       = aws_dynamodb_table.process_state_table.name
}

output "process_state_table_arn" {
  description = "The ARN of the Process State DynamoDB table"
  value       = aws_dynamodb_table.process_state_table.arn
}

output "user_table_name" {
  description = "The name of the User DynamoDB table"
  value       = aws_dynamodb_table.user_table.name
}

output "user_table_arn" {
  description = "The ARN of the User DynamoDB table"
  value       = aws_dynamodb_table.user_table.arn
}