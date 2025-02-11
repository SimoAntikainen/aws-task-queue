import os
import boto3
import json
from dotenv import load_dotenv

load_dotenv()

SQS_QUEUE_URL = os.environ["SQS_QUEUE_URL"]
REGION_NAME= os.environ["REGION_NAME"]
sqs_client = boto3.client("sqs", region_name=REGION_NAME)

def fetch_messages_by_batch_from_sqs(batch_id, max_messages=10, wait_time=10):
    """
    Fetch messages from SQS FIFO queue for a specific batchId using Message Attributes.
    :param batch_id: The batch ID to filter messages.
    :param max_messages: Number of messages to retrieve at once.
    :param wait_time: How long to wait for messages (long polling).
    """
    messages = []

    try:
        response = sqs_client.receive_message(
            QueueUrl=SQS_QUEUE_URL,
            MaxNumberOfMessages=max_messages,
            WaitTimeSeconds=wait_time,
            MessageAttributeNames=["All"],
            AttributeNames=["MessageGroupId"]  # Retrieve batchId group
        )

        if "Messages" in response:
            for message in response["Messages"]:
                batch_id_attr = message.get("MessageAttributes", {}).get("batchId", {}).get("StringValue", "")

                if batch_id_attr == batch_id:
                    messages.append(json.loads(message["Body"]))

                    # Delete message from queue after processing
                    sqs_client.delete_message(
                        QueueUrl=SQS_QUEUE_URL,
                        ReceiptHandle=message["ReceiptHandle"]
                    )
                    print(f"Deleted message: {message['Body']}")

        return messages

    except Exception as e:
        print(f"Error fetching messages from SQS: {e}")
        return []