## Setting up dev environment


## Python tooling

```
sudo apt update

sudo apt install python3 python3-venv python3-pip -y

python3 -m venv devenv
source devenv/bin/activate

pip install boto3
```

## AWS tooling


### AWS CLI

https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html 
```
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

https://docs.aws.amazon.com/cli/latest/userguide/getting-started-quickstart.html
Create AWS user with SSO or long term access key in IAM.
```
aws configure sso
or
aws configure
=> fill in the info
```

### Terraform
https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli






## VS Code extensions

The following extensions are useful:

ms-python.python
hashicorp.terraform


