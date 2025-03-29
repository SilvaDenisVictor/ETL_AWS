data "archive_file" "lambda" {
  type        = "zip"
  source_file = "code/lambda_code.py"
  output_path = "code/lambda_code.zip"
}

resource "aws_lambda_function" "etl-bitcoin-lambda" {
  filename      = data.archive_file.lambda.output_path
  function_name = "${var.bucket_name}-lambda-function"
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "lambda_code.lambda_handler"
  timeout       = 600

  source_code_hash = data.archive_file.lambda.output_base64sha256

  runtime = "python3.10"

  environment {
    variables = {
      CRAWLER_NAME  = aws_glue_crawler.etl_bitcoin_crawler.name
      GLUE_JOB_NAME = aws_glue_job.etl_bitcoin.name
    }
  }
}

resource "aws_lambda_permission" "allow_s3_to_invoke" {
  statement_id  = "AllowExecutionFromS3"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.etl-bitcoin-lambda.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = data.aws_s3_bucket.etl-bitcoin.arn
}

resource "aws_s3_bucket_notification" "etl-bitcoin-trigger" {
  bucket = data.aws_s3_bucket.etl-bitcoin.id

  lambda_function {
    events              = ["s3:ObjectCreated:*"]
    filter_prefix       = "raw/"
    filter_suffix       = ".csv"
    lambda_function_arn = aws_lambda_function.etl-bitcoin-lambda.arn
  }

  depends_on = [aws_lambda_function.etl-bitcoin-lambda]
}