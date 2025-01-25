resource "aws_s3_bucket" "task_bucket" {
  bucket = var.bucket_name
  tags = var.tags         

}

output "bucket_name" {
  value = aws_s3_bucket.task_bucket.bucket
}

output "bucket_arn" {
  value = aws_s3_bucket.task_bucket.arn
}