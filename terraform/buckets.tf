# S3 Bucket for Source Data
# resource "aws_s3_bucket" "etl-bitcoin" {
#   bucket        = var.bucket_name
#   force_destroy = false
# }

# Refering a existing bucket
data "aws_s3_bucket" "etl-bitcoin" {
  bucket = var.bucket_name
}


# Carregando o script para a pasta 'script' no bucket S3
resource "aws_s3_object" "script_etl" {
  bucket = data.aws_s3_bucket.etl-bitcoin.bucket
  key    = "script/script_etl.py"
  source = "code/script_bitcoin.py"
}