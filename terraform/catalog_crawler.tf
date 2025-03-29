# Create Glue Data Catalog Database
resource "aws_glue_catalog_database" "etl_bitcoin_database" {
  name         = "${var.bucket_name}-database"
  location_uri = "${data.aws_s3_bucket.etl-bitcoin.id}/"
}


# Create Glue Crawler
resource "aws_glue_crawler" "etl_bitcoin_crawler" {
  name          = "${var.bucket_name}-crawler"
  database_name = aws_glue_catalog_database.etl_bitcoin_database.name
  role          = aws_iam_role.glue_service_role.name
  s3_target {
    path = "${data.aws_s3_bucket.etl-bitcoin.id}/transformed/"
  }

  s3_target {
    path = "${data.aws_s3_bucket.etl-bitcoin.id}/raw/"
  }

  schema_change_policy {
    delete_behavior = "LOG"
  }

  configuration = jsonencode(
    {
      Grouping = {
        TableGroupingPolicy = "CombineCompatibleSchemas"
      }
      CrawlerOutput = {
        Partitions = { AddOrUpdateBehavior = "InheritFromTable" }
      }
      Version = 1
    }
  )
}

# Create Glue Trigger
resource "aws_glue_trigger" "org_report_trigger" {
  name = "${var.bucket_name}-trigger"
  type = "ON_DEMAND"
  actions {
    crawler_name = aws_glue_crawler.etl_bitcoin_crawler.name
  }
}