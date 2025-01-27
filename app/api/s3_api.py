import uuid
from datetime import datetime
from urllib.parse import quote
import requests
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError


def generate_object_key(app_name:str, environment:str, user_id:str, task_id:str, filename:str, task_type: str, resource_type="upload"):
    """
    Generate a unique key using the provided parameters.

    :param app_name: Name of the application
    :param environment: Application environment (e.g, Development | Staging | Production)
    :param user_id: Unique User identifier
    :param task_id: Unique task identifier
    :param task_type: Type of the task, which defines workflow after file is uploaded to s3
    :param filename: Name of the file uploaded to s3
    :param resource_type:  Type or purpose of the resource (e.g., upload, processed, results, logs)
    """

    key = f"{app_name}/{environment}/account/{user_id}/{task_id}/{task_type}/{resource_type}/{filename}"
    return key


def generate_presigned_url(bucket_name, object_key, expiration=3600, operation="put_object"):
    """
    Generate a pre-signed URL for an S3 object.

    :param bucket_name: Name of the S3 bucket
    :param object_key: The key of the object in the S3 bucket
    :param expiration: Time in seconds for the pre-signed URL to remain valid (default: 3600 seconds)
    :param operation: The S3 operation (default: "put_object", can also be "get_object")
    :return: Pre-signed URL as a string
    """
    try:
        s3_client = boto3.client("s3")

        url = s3_client.generate_presigned_url(
            ClientMethod=operation,
            Params={"Bucket": bucket_name, "Key": object_key},
            ExpiresIn=expiration,
        )
        return url

    except NoCredentialsError:
        raise RuntimeError("AWS credentials not available.")
    except PartialCredentialsError:
        raise RuntimeError("Incomplete AWS credentials provided.")
    except Exception as e:
        raise RuntimeError(f"An error occurred while generating the pre-signed URL: {e}")
    

def upload_file_to_s3(bucket_name, object_key, file_path):
    """
    Upload a file to S3.

    :param bucket_name: Name of the S3 bucket.
    :param object_key: The key for the S3 object.
    :param file_path: Path to the local file to upload.
    """
    s3_client = boto3.client("s3")
    try:
        # Upload the file
        s3_client.upload_file(file_path, bucket_name, object_key)
        print(f"File uploaded successfully: {file_path} -> s3://{bucket_name}/{object_key}")
    except Exception as e:
        print(f"Error uploading file {file_path} to S3: {e}")
        raise RuntimeError(f"Failed to upload {file_path} to S3.")
    

def upload_file_with_presigned_url(file_path, presigned_url):
    """
    Upload a file to S3 using a pre-signed URL.

    :param file_path: Path to the local file to upload.
    :param presigned_url: Pre-signed URL for uploading the file.
    """
    try:
        with open(file_path, "rb") as file_data:
            response = requests.put(presigned_url, data=file_data)
            if response.status_code == 200:
                print(f"File uploaded successfully: {file_path}")
            else:
                raise RuntimeError(
                    f"Failed to upload file {file_path}. HTTP Status: {response.status_code}, Response: {response.text}"
                )
    except Exception as e:
        raise RuntimeError(f"Error uploading file {file_path} using pre-signed URL: {e}")