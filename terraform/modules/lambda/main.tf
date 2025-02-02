resource "aws_iam_role" "lambda_role" {
  name = "lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_policy" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}



resource "aws_iam_policy" "dynamodb_policy" {
  name        = "dynamodb-access-policy"
  description = "Policy to allow Lambda access to update the ProcessStateTable in DynamoDB"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = [
          "dynamodb:UpdateItem",
          "dynamodb:GetItem",
          "dynamodb:Query"
        ]
        Resource = "arn:aws:dynamodb:${var.region}:${var.account_id}:table/ProcessStateTable"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_dynamodb_policy" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.dynamodb_policy.arn
}

#resource "aws_lambda_permission" "allow_s3_invocation" {
#  statement_id  = "AllowS3Invocation"
#  action        = "lambda:InvokeFunction"
#  function_name = module.lambda.s3_upload_completed_lambda_arn
#  principal     = "s3.amazonaws.com"
#  source_arn    = module.s3.bucket_arn
#}




resource "aws_lambda_function" "my_lambda" {
  filename         = "${path.module}/../../../app/lambda/lambda_function.zip"
  function_name    = "my_lambda_function"
  role             = aws_iam_role.lambda_role.arn
  handler          = "lambda_function.handler"
  runtime          = "python3.12" # Change based on your runtime
  source_code_hash = filebase64sha256("${path.module}/../../../app/lambda/lambda_function.zip")
  tags = var.tags 
}

resource "aws_lambda_function" "s3_upload_completed_lambda" {
  filename         = "${path.module}/../../../app/lambda/s3_upload_completed.zip"
  function_name    = "s3_upload_completed"
  role             = aws_iam_role.lambda_role.arn
  handler          = "s3_upload_completed.handler"
  runtime          = "python3.12" # Change based on your runtime
  source_code_hash = filebase64sha256("${path.module}/../../../app/lambda/s3_upload_completed.zip")
  tags = var.tags 
}

resource "aws_lambda_permission" "allow_s3" {
  statement_id  = "AllowExecutionFromS3"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.s3_upload_completed_lambda.arn
  principal     = "s3.amazonaws.com"
  # Using the bucket ARN to restrict permission to just this bucket
  source_arn    = var.s3_bucket_arn
}

resource "aws_s3_bucket_notification" "notify_lambda" {
  bucket = var.s3_bucket_name

  lambda_function {
    lambda_function_arn = aws_lambda_function.s3_upload_completed_lambda.arn
    events              = ["s3:ObjectCreated:*"]
    filter_prefix = "AIDetectionApp/Development/account/upload/"
    # filter_suffix = ".jpg"
  }

  # Ensure that the lambda permission is created before the notification
  depends_on = [aws_lambda_permission.allow_s3]
}