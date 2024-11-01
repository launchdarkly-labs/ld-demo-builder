data "archive_file" "demobuilder_zip" {
  type             = "zip"
  source_dir       = "${path.module}/demobuilder"
  excludes         = ["${path.module}/demobuilder/lambda_demobuilder.zip"]
  output_file_mode = "0666"
  output_path      = "${path.module}/demobuilder/lambda_demobuilder.zip"
  depends_on = [
    null_resource.python_pytz,
    null_resource.python_randomname,
    null_resource.python_requests
  ]
}

resource "aws_lambda_function" "lambda_demobuilder" {
  # If the file is not in the current working directory you will need to include a
  # path.module in the filename.
  filename      = "${path.module}/demobuilder/lambda_demobuilder.zip"
  function_name = local.demobuilder_fname
  role          = aws_iam_role.lambda_iam_role.arn
  architectures = ["x86_64"]
  # layers           = ["arn:aws:lambda:us-east-2:336392948345:layer:AWSSDKPandas-Python39:13"]
  handler          = "wrapper.lambda_handler"
  source_code_hash = data.archive_file.demobuilder_zip.output_base64sha256
  runtime          = "python3.11"
  timeout          = 900
  environment {
    variables = {
      LOG_GROUP       = local.demobuilder_loggroup
      LD_API_KEY      = var.ld_api_key
      LD_API_KEY_USER = var.ld_api_key_user
      DDB_TABLE       = aws_dynamodb_table.demo_tracker.name
    }
  }

  depends_on = [
    data.archive_file.demobuilder_zip
  ]
}

resource "aws_lambda_function_url" "lambda_demobuilder_url" {
  function_name      = aws_lambda_function.lambda_demobuilder.arn
  authorization_type = "NONE"

  cors {
    allow_credentials = false
    allow_origins     = ["*"]
    allow_methods     = ["POST", "GET"]
    allow_headers     = ["*"]
    expose_headers    = ["keep-alive", "date"]
    max_age           = 86400
  }

  depends_on = [aws_lambda_function.lambda_demobuilder]
}

resource "aws_cloudwatch_log_group" "lambda_log_demobuilder" {
  name              = local.demobuilder_loggroup
  retention_in_days = 14
  lifecycle {
    prevent_destroy = false
  }
}

resource "aws_cloudwatch_log_stream" "lambda_logstream_demobuilder" {
  name           = "ApplicationLogs"
  log_group_name = aws_cloudwatch_log_group.lambda_log_demobuilder.name
}

resource "aws_iam_role" "lambda_iam_role" {
  name = "${var.unique_identifier}-iam-for-lambda"

  assume_role_policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        Action : "sts:AssumeRole",
        Effect : "Allow",
        Principal : {
          "Service" : "lambda.amazonaws.com"
        }
      }
    ]
  })
}

data "aws_iam_policy_document" "lambda_access_policy" {
  statement {
    sid       = "FullAccess"
    effect    = "Allow"
    resources = ["*"]

    actions = [
      "dynamodb:PutItem",
      "dynamodb:Query",
      "dynamodb:Scan",
      "dynamodb:Get*",
      "dynamodb:Update*",
      "dynamodb:Delete*",
      "s3:*"
    ]
  }
}

resource "aws_iam_policy" "lambda_logging_policy" {
  name = "${var.unique_identifier}-lambda-logging-policy"
  policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        Action : [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        Effect : "Allow",
        Resource : "arn:aws:logs:*:*:*"
      }
    ]
  })
}

resource "aws_iam_role_policy" "lambda_iam_access_policy" {
  name   = "${var.unique_identifier}-lambda-access-policy"
  role   = aws_iam_role.lambda_iam_role.id
  policy = data.aws_iam_policy_document.lambda_access_policy.json
}

resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.lambda_iam_role.id
  policy_arn = aws_iam_policy.lambda_logging_policy.arn
}
