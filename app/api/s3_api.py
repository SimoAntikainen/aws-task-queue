import uuid
from datetime import datetime
from urllib.parse import quote
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError


def generate_object_key(app_name:str, environment:str, user_id:str, task_id:str, filename:str, resource_type="upload"):
    """
    Generate a unique key using the provided parameters.

    :param app_name: Name of the application
    :param environment: Application environment (e.g, Development | Staging | Production)
    :param user_id: Unique User identifier
    :param task_id: Unique task identifier 
    :param filename: Name of the file uploaded to s3
    :param resource_type:  Type or purpose of the resource (e.g., upload, processed, results, logs)
    """

    key = f"{app_name}/{environment}/account/{user_id}/{task_id}/{resource_type}/{filename}"
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