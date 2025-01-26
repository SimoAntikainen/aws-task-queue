import uuid
from datetime import datetime
from api.dynamodb_api import create_task_in_dynamodb, fetch_tasks_from_dynamodb,  fetch_tasks_by_batch_from_dynamodb
from api.s3_api import generate_object_key, generate_presigned_url

APP_NAME = 'AIDetectionApp'
ENVIRONMENT = 'Development'

def generate_batch_id():
    """
    Generate a unique batch_id using UUID.
    """
    return str(uuid.uuid4())

def generate_task_id_with_timestamp():
    """
    Generate a unique task_id using UUID.
    """
    timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    id = timestamp + '_' +str(uuid.uuid4())
    return id, timestamp


    
if __name__ == "__main__":
    # Example usage
    bucket_name = "ai-detection-app-dev-task-bucket"
    expire_task_time = 7200 # 2 hours
    expiration_time = 3600  # 1 hour

    app_name = APP_NAME
    environment = ENVIRONMENT
    user_id = "user123"
    filenames = ["input-image.jpg",  "cat.jpg", "file with special characters @#!.txt" ]


    batch_id = generate_batch_id()
    
    for filename in filenames:
        task_id, timestamp = generate_task_id_with_timestamp()
        object_key = generate_object_key(app_name, environment, user_id, task_id, filename)
        print(f"Generated Object Key: {object_key}")
        create_task_in_dynamodb(bucket_name, user_id, task_id, batch_id, timestamp, object_key, expire_task_time)

        try:
            url = generate_presigned_url(bucket_name, object_key, expiration=expiration_time)
            print(f"Pre-signed URL: {url}")
        except RuntimeError as error:
            print(f"Error: {error}")
    


    #tasks = fetch_tasks_by_batch_from_dynamodb(batch_id)
    #if tasks:
    #    print("Fetched Batch of Tasks:")
    #    for task in tasks:
    #        print(task)
    



    '''
    object_key = generate_object_key(app_name, environment, user_id, task_id, filename)
    print(f"Generated Object Key: {object_key}")

    filename = "cat.jpg"
    object_key = generate_object_key(app_name, environment, user_id, task_id, filename)
    print(f"Generated Object Key: {object_key}")
    create_task_in_dynamodb(bucket_name, user_id, task_id, object_key)

    try:
        url = generate_presigned_url(bucket_name, object_key, expiration=expiration_time)
        print(f"Pre-signed URL: {url}")
    except RuntimeError as error:
        print(f"Error: {error}")'''


