resource "aws_dynamodb_table" "process_state_table" {
  name         = "ProcessStateTable"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "userId"
  range_key    = "taskId"

  attribute {
    name = "userId"
    type = "S"
  }

  attribute {
    name = "taskId"
    type = "S"
  }

  attribute {
    name = "batchId"
    type = "S" # To uniquely identify the batch of created tasks
  }

  global_secondary_index {
    name            = "batchIdIndex"
    hash_key        = "batchId"
    range_key       = "taskId"
    projection_type = "ALL"
  }

  // https://stackoverflow.com/questions/40561484/what-data-type-should-be-used-for-timestamp-in-dynamodb
  ttl {
    attribute_name = "expireAt" # Enable TTL on this attribute (eg. one day-> after completedAt)
    enabled        = true
  }

  /* defining other attributes here for documentation

  attribute {
    name = "taskType"
    type = "S" # type of the task, which defines workflow after file is uploaded to s3
  }

  attribute {
    name = "status"
    type = "S" # String (processing | completed)
  }

  attribute {
    name = "createdDate"
    type = "S" # String (ISO 8601 timestamps like "2023-01-25T12:00:00Z")
  }

  attribute {
    name = "completedDate"
    type = "S" # String (ISO 8601 timestamps like "2023-01-25T12:00:00Z")
  }

  attribute {
    name = "expireAt"
    type = "N" # TTL attribute (UNIX epoch time)
  }

  attribute {
    name = "file_s3_link"
    type = "S" # String (URL format)
  }

  attribute {
    name = "results_s3_link"
    type = "S" # String (URL format)
  }
  */

  tags = var.tags  
}


resource "aws_dynamodb_table" "user_table" {
  name           = "UserTable"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "userId"

  attribute {
    name = "userId"
    type = "S" 
  }

  tags = var.tags  
}