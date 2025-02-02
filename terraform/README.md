
## Applying terraform 

If you are using this project as a basis for your code ìn `environments/.../terraform.tfvars` change
the `s3` bucket `task_bucket_name` to some unique bucket name. 

```
region          = "eu-west-1"
task_bucket_name  = "ai-detection-app-dev-task-bucket"
environment     = "Development"
project         = "AIDetectionApp"
```

Then navigate to `cd/enviroments/dev`

```
terraform init
terraform plan
terraform apply
```

terraform apply -target=module.dynamodb
terraform destroy -target=module.dynamodb

if you modify the `app/api/lambda` remember to zip them






### Tables

ProcessStateTable:
id
userId
created
completed
image_s3_link
results_s3_link






attribute {
    name = "completed"
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

  // https://stackoverflow.com/questions/40561484/what-data-type-should-be-used-for-timestamp-in-dynamodb
  ttl {
    attribute_name = "expireAt" # Enable TTL on this attribute (eg. one day-> after completedAt)
    enabled        = true
  }

  attribute {
    name = "image_s3_link"
    type = "S" # String (URL format)
  }

  attribute {
    name = "results_s3_link"
    type = "S" # String (URL format)
  }