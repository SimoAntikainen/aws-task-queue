# AWS Task Queue Boilerplate



## Setting up and running the project

After the underlying steps are completed you should be able to run `app/process_files_in_task.py` script, which runs the task queue with test data in `app/example_data` and writes their results to `app/results` upon succesfull processing. Currently the only task implemented is summarization of text via claude 3.5


### Python

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip -y

python3 -m venv devenv
source devenv/bin/activate

pip install -r requirements.txt
```

### Terraform
https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli


### AWS tooling

#### AWS CLI

https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html 
```
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

#### IAM user

https://docs.aws.amazon.com/cli/latest/userguide/getting-started-quickstart.html
Create AWS user with SSO or long term access key in IAM with access to used AWS resources for terraform.
```
aws configure sso
or
aws configure
=> fill in the info
```

The underlying table gives an idea of the used services and permissions:

| Resource                  | Minimum Permission                      |
|---------------------------|-----------------------------------------|
| **S3**                    | `s3:*`                                  |
| **Lambda**                | `lambda:*`                              |
| **IAM (for Lambda roles)** | `iam:CreateRole`, `iam:AttachRolePolicy`, `iam:PassRole` |
| **CloudWatch Logs**        | `logs:*`                               |
| **DynamoDB** | `dynamodb:*`                  |
| **API Gateway** | `apigateway:*`                        |
| **SQS**                   | `sqs:*`                                 |
| **Bedrock**               | `bedrock:*`                             |




#### AWS Bedrock

For bedrock You might need to separately request access rights for your account
https://docs.aws.amazon.com/bedrock/latest/userguide/getting-started.html


### VS Code extensions

The following extensions are useful:

* [ms-python.python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
* [hashicorp.terraform](https://marketplace.visualstudio.com/items?itemName=HashiCorp.terraform)
* [Ruff](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff)


## Environment variables


___

## TODO:s

* Retry mechanisms for failed tasks
* Use strong consistency mode to DynamoDB or add retries for updating task state (There is a small change task is not created fast enough). https://stackoverflow.com/questions/55306845/is-dynamodb-item-available-for-querying-immediately



## Useful resources

https://github.com/awsdocs/aws-doc-sdk-examples/blob/main/python/example_code/



