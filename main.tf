terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.38.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.6.0"
    }
    archive = {
      source  = "hashicorp/archive"
      version = "~> 2.4.2"
    }
  }
  required_version = "~> 1.2"
}

resource "aws_lambda_function" "function" {
  filename                       = "quantegy-analyze.zip"
  function_name                  = "analyse-market-data-prod"
  handler                        = "evangeline.main"
  runtime                        = "python3.9"
  timeout                        = 900
  reserved_concurrent_executions = 1
  memory_size                    = 128
  role                           = "arn:aws:iam::716418748259:role/quantegy-analyze-soak-us-east-1-lambdaRole"
}

data "archive_file" "function_zip" {
  source_dir  = ${path.module}
  type        = "zip"
  output_path = "quantegy-analyze.zip"
}