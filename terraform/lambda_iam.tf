data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

# Política separada para permissões de Glue
data "aws_iam_policy_document" "glue_permissions" {
  statement {
    effect = "Allow"
    actions = [
      "glue:StartJobRun",
      "glue:GetJobRun",
      "glue:GetJobRuns",
      "glue:GetJobs"
    ]
    resources = [aws_glue_job.etl_bitcoin.arn]
  }

  statement {
    effect = "Allow"
    actions = [
      "glue:StartCrawler",
      "glue:GetCrawler",
      "glue:GetCrawlers"
    ]

    resources = [aws_glue_crawler.etl_bitcoin_crawler.arn]
  }

  statement {
    effect  = "Allow"
    actions = ["lambda:InvokeFunction"]

    resources = [aws_lambda_function.etl-bitcoin-lambda.arn]
  }

  statement {
    effect    = "Allow"
    resources = ["arn:aws:logs:*:*"]
    actions   = ["logs:CreateLogGroup"]
  }

  statement {
    effect    = "Allow"
    resources = ["arn:aws:logs:*:*:log-group:/aws/lambda/*:*"]

    actions = [
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]
  }

}

resource "aws_iam_role" "iam_for_lambda" {
  name               = "iam_for_lambda"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

# Associe a política de permissões do Glue ao role
resource "aws_iam_role_policy" "glue_policy_for_lambda" {
  name   = "glue-policy-for-lambda"
  role   = aws_iam_role.iam_for_lambda.id
  policy = data.aws_iam_policy_document.glue_permissions.json
}
