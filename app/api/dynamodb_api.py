from datetime import datetime, timedelta
import boto3
from botocore.exceptions import ClientError

def create_task_in_dynamodb(bucket_name: str, user_id: str, task_id: str, batch_id: str, created_date: str, object_key: str, expire_seconds: 3600):
    """
    Create a task entry in DynamoDB.
    """
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("ProcessStateTable") 

    # Set expiration time
    created_date_obj = datetime.strptime(created_date, "%Y-%m-%dT%H:%M:%SZ")
    expire_at = int((created_date_obj + timedelta(seconds=expire_seconds)).timestamp())

    # future_date_obj = created_date_obj + timedelta(days=1)
    # future_date = future_date_obj.strftime("%Y-%m-%dT%H:%M:%SZ")
    # print("Created Date:", created_date)
    # print("Future Date:", future_date)

    try:
        table.put_item(
            Item={
                "userId": user_id,
                "taskId": task_id,
                "batchId" : batch_id,
                "createdDate": created_date,
                "status": "processing",  # Initial status
                "file_s3_link": f"s3://{bucket_name}/{object_key}",
                "results_s3_link": "",  # Results link will be updated later
                "expireAt": expire_at,
            }
        )
        print(f"Task {task_id} created in DynamoDB.")
    except Exception as e:
        raise RuntimeError(f"Failed to create task in DynamoDB: {e}")
    
    return created_date


def fetch_tasks_from_dynamodb(user_id, task_id=None):
    """
    Fetch tasks from DynamoDB filtered by userId and optionally by taskId.

    :param user_id: The userId to filter tasks by.
    :param task_id: (Optional) The taskId to filter tasks by.
    :return: A list of tasks matching the filters.
    """
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("ProcessStateTable") 

    try:
        if task_id:
            # Query with both userId and taskId (Exact Match)
            response = table.get_item(
                Key={
                    "userId": user_id,
                    "taskId": task_id,
                }
            )
            task = response.get("Item")
            if task:
                return [task]
            else:
                return []  # No matching task found
        else:
            # Query by userId only (Fetch all tasks for the user)
            response = table.query(
                KeyConditionExpression=boto3.dynamodb.conditions.Key("userId").eq(user_id)
            )
            return response.get("Items", [])

    except ClientError as e:
        print(f"An error occurred: {e}")
        raise RuntimeError("Failed to fetch tasks from DynamoDB.")
    

def fetch_tasks_by_batch_from_dynamodb(batch_id):
    """
    Query tasks for a specific user and batchId.
    :param batch_id: The batchId to filter tasks by.
    :return: A list of tasks matching the filters.
    """
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("ProcessStateTable") 

    try:
        # Query the GSI for tasks by batchId
        response = table.query(
        IndexName="batchIdIndex",
        KeyConditionExpression=boto3.dynamodb.conditions.Key("batchId").eq(batch_id)
        )
        tasks = response.get("Items", []) 
        return tasks

    except ClientError as e:
        print(f"An error occurred: {e}")
        raise RuntimeError("Failed to query tasks from DynamoDB.")

