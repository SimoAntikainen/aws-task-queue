# Create a FIFO Dead-Letter Queue (DLQ)
resource "aws_sqs_queue" "results_queue_dlq" {
  name       = "ResultsQueueDLQ.fifo"
  fifo_queue = true
}

resource "aws_sqs_queue" "results_queue" {
  name                        = "ResultsQueue.fifo"
  fifo_queue                  = true
  content_based_deduplication = true  # Enable deduplication

  visibility_timeout_seconds = 30   # Ensures Lambda has time to process the message before making it visible again
  message_retention_seconds  = 86400  # 1 day retention
  delay_seconds              = 0
  max_message_size           = 262144  # 256 KB
  receive_wait_time_seconds  = 0

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.results_queue_dlq.arn
    maxReceiveCount     = 5
  })
}