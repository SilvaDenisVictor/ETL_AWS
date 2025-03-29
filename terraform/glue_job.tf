resource "aws_glue_job" "etl_bitcoin" {
  name              = "${var.bucket_name}-glue-job"
  role_arn          = aws_iam_role.glue_service_role.arn
  description       = "Removing invalid values."
  glue_version      = "4.0"
  worker_type       = "G.1X"
  timeout           = 60
  max_retries       = 1
  number_of_workers = 2
  command {
    name            = "glueetl"
    python_version  = 3
    script_location = "s3://${data.aws_s3_bucket.etl-bitcoin.bucket}/${aws_s3_object.script_etl.key}"
  }

  default_arguments = {
    "--enable-auto-scaling"              = "true"
    "--enable-continuous-cloudwatch-log" = "true"
    "--datalake-formats"                 = "delta"
    "--source-path"                      = "s3://${data.aws_s3_bucket.etl-bitcoin.bucket}/raw/"
    "--destination-path"                 = "s3://${data.aws_s3_bucket.etl-bitcoin.bucket}/transformed/"
    "--job-name"                         = "${var.bucket_name}-glue-job"
    "--enable-continuos-log-filter"      = "true"
    "--enable-metrics"                   = "true"
  }

}