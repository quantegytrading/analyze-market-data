terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.38.0"
    }
  }
  required_version = "~> 1.2"
}

resource "aws_lambda_function" "function" {
  s3_bucket                      = "quantegy-analyze-soak-us-east-1-lambda"
  s3_key                         = "quantegy-analyze.zip"
  function_name                  = "analyse-market-data-prod"
  handler                        = "evangeline.main"
  runtime                        = "python3.9"
  timeout                        = 900
  reserved_concurrent_executions = 1
  memory_size                    = 128
  role                           = "arn:aws:iam::716418748259:role/quantegy-analyze-soak-us-east-1-lambdaRole"
}