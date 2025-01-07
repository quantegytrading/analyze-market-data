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
  s3_bucket                       = "quantegy-analyze-soak-us-east-1-lambda"
  s3_key                          = "quantegy-analyze.zip"
  function_name                   = "quantegy-analyze"
  handler                        = "evangeline.main"
  runtime                        = "python3.9"
  timeout                        = 900
  memory_size                    = 128
  role                           = "arn:aws:iam::716418748259:role/quantegy-analyze-soak-us-east-1-lambdaRole"
}



data "archive_file" "function_zip" {
  source_dir  = "src"
  type        = "zip"
  output_path = "${path.module}/quantegy-analyze.zip"
}

resource "aws_s3_object" "file_upload" {
  bucket = "quantegy-analyze-soak-us-east-1-lambda"
  key    = "quantegy-analyze.zip"
  source = "quantegy-analyze.zip"
  depends_on = [
    data.archive_file.function_zip
  ]
}