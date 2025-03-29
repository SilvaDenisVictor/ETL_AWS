variable "aws_region" {
  description = "AWS region to deploy resources"
  default     = "us-east-1"
}

variable "bucket_name" {
  description = "Bucket name."
  default     = "etl-bitcoin-151548481919"
  type        = string
}