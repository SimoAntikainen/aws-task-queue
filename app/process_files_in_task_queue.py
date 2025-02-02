import os
import uuid
import time
from datetime import datetime
from api.dynamodb_api import create_task_in_dynamodb, fetch_tasks_from_dynamodb,  fetch_tasks_by_batch_from_dynamodb
from api.s3_api import generate_object_key, generate_presigned_url, upload_file_to_s3, upload_file_with_presigned_url

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


    files = [{
        'file_path' : 'app/example_data/moby_dick.txt',
        'task_type' : 'translate'
    },
    {
        'file_path' : 'app/example_data/file with special characters @#!.txt',
        'task_type' : 'translate'
    }
    ]


    batch_id = generate_batch_id()
    
    for file in files:
        file_path = file['file_path']
        file_name = os.path.basename(file['file_path'])
        task_type = file['task_type']

        task_id, timestamp = generate_task_id_with_timestamp()
        object_key = generate_object_key(app_name, environment, user_id, task_id, task_type, file_name)
        print(f"Generated Object Key: {object_key}")
        create_task_in_dynamodb(bucket_name, user_id, task_id, batch_id, task_type, timestamp, object_key, expire_task_time)

        try:
            url = generate_presigned_url(bucket_name, object_key, expiration=expiration_time)
            print(f"Pre-signed URL: {url}")
            #upload_file_to_s3(bucket_name, object_key, file_path)
            upload_file_with_presigned_url(file_path, url)

        except RuntimeError as error:
            print(f"Error: {error}")




        
    time.sleep(10)

    tasks = fetch_tasks_by_batch_from_dynamodb(batch_id)
    if tasks:
        print("Fetched Batch of Tasks:")
        for task in tasks:
            print(task)
    



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


