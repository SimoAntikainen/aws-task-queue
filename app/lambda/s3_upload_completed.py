import json
import boto3
from urllib.parse import unquote
from botocore.exceptions import ClientError







def handler(event, context):
    """
    AWS Lambda function triggered by an S3 event to update the status
    in the DynamoDB ProcessStateTable after an S3 upload is complete.

    :param event: Event data from S3 trigger
    :param context: AWS Lambda context object
    """
    # Initialize DynamoDB resource
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("ProcessStateTable")  # Ensure this matches your table name
    lambda_client = boto3.client("lambda")
    s3_client = boto3.client("s3")

    try:
        # Loop through S3 event records
        for record in event['Records']:
            # Extract bucket and object key from the event
            bucket_name = record['s3']['bucket']['name']
            raw_object_key = record['s3']['object']['key']
            
            print(f"raw key: {raw_object_key}")

            # Decode URL-encoded object key
            object_key = unquote(raw_object_key)
            print(f"Processing object: {object_key} in bucket: {bucket_name}")
            
            # debug code
            s3_response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
            #text = s3_response["Body"].read().decode("utf-8")
            print(f"Retrieved text from s3://{bucket_name}/{object_key}")

            # Extract userId and taskId from the object key
            key_parts = object_key.split("/")

            app_name, environment, resource_type, _, user_id, task_type, task_id, filename = key_parts

            # Query and update the DynamoDB table
            response = table.update_item(
                Key={
                    "userId": user_id,
                    "taskId": task_id
                },
                UpdateExpression="SET #status = :new_status",
                ExpressionAttributeNames={
                    "#status": "status"
                },
                ExpressionAttributeValues={
                    ":new_status": "uploaded"
                },
                ReturnValues="UPDATED_NEW"
            )

            print(f"Updated status for task {task_id}: {response['Attributes']}")


            payload = {
                    "bucket": bucket_name,
                    "object_key": raw_object_key,
                    "app_name": app_name,
                    "environment": environment,
                    "user_id": user_id,
                    "task_id": task_id,
                    "filename": filename
            }

            print(f"payload: {payload}")

            if task_type == 'summarize':
                lambda_client.invoke(
                    FunctionName="summarize_text",
                     InvocationType="Event",      
                    Payload=json.dumps(payload)
                )

            

    except KeyError as e:
        print(f"KeyError: {e}. Event: {json.dumps(event)}")
        raise RuntimeError("Invalid S3 event structure.")
    except ClientError as e:
        print(f"DynamoDB Error: {e}")
        raise RuntimeError("Failed to update DynamoDB.")
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise RuntimeError("Error processing S3 event.")

    return {
        "statusCode": 200,
        "body": json.dumps("Status updated successfully.") 
    }