import os
from urllib.parse import quote
import uuid
import time
from datetime import datetime
from dotenv import load_dotenv

from api.dynamodb_api import create_task_in_dynamodb, fetch_tasks_from_dynamodb,  fetch_tasks_by_batch_from_dynamodb
from api.s3_api import generate_object_key, generate_presigned_url, upload_file_to_s3, upload_file_with_presigned_url
from api.sqs_api import fetch_messages_by_batch_from_sqs

load_dotenv()

APP_NAME = os.environ["APP_NAME"] 
ENVIRONMENT = os.environ["ENVIRONMENT"]  
BUCKET_NAME = os.environ["BUCKET_NAME"]  

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

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
    bucket_name = BUCKET_NAME
    expire_task_time = 7200 # 2 hours
    expiration_time = 3600  # 1 hour

    app_name = APP_NAME
    environment = ENVIRONMENT
    user_id = "user123"


    files = [{
        'file_path' : CURRENT_DIR + '/example_data/moby_dick.txt',
        'task_type' : 'summarize'
    },
    {
        'file_path' : CURRENT_DIR +'/example_data/file with special characters @#!.txt',
        'task_type' : 'summarize'
    }
    ]


    batch_id = generate_batch_id()
    task_ids = set()
    for file in files:
        file_path = file['file_path']
        file_name = os.path.basename(file['file_path'])
        task_type = file['task_type']


        task_id, timestamp = generate_task_id_with_timestamp()
        task_ids.add(task_id)
        object_key = generate_object_key(app_name, environment, user_id, task_id, task_type, file_name)
        print(f"Generated Object Key: {object_key}")
        create_task_in_dynamodb(bucket_name, user_id, task_id, batch_id, task_type, timestamp, object_key, expire_task_time)

        try:
            url = generate_presigned_url(bucket_name, object_key, expiration=expiration_time)
            # use pe-signed url just for demonstration purposes
            #upload_file_to_s3(bucket_name, object_key, file_path)
            print(f"Pre-signed URL: {url}")
            upload_file_with_presigned_url(file_path, url)

        except RuntimeError as error:
            print(f"Error: {error}")
            raise


    time.sleep(5)

    print(f"\n🟢 Fetching Batch Task State for batchId {batch_id}...")
    tasks = fetch_tasks_by_batch_from_dynamodb(batch_id)
    if tasks:
        print("Fetched Batch of Tasks:")
        for task in tasks:
            print(task)


    print(f"\n🟢 Polling for Task completion messages from SQS by batchId {batch_id}...")

    while task_ids:
        print(f"🔄 Polling SQS... Waiting for {len(task_ids)} remaining tasks.")
    
        sqs_messages = fetch_messages_by_batch_from_sqs(batch_id, wait_time=10)

        if sqs_messages:
            print("\n✅ Completed Task Messages from SQS:")
            for msg in sqs_messages:
                task_id = msg['taskId']
                print(msg)
                if task_id in task_ids:
                    task_ids.remove(task_id)
        else:
            print("\n⚠️ No messages found in SQS for batchId:", batch_id)

        # Small delay before the next poll to avoid excessive requests
        time.sleep(5)



    

