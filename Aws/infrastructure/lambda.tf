resource "aws_lambda_function" "parser-lambda" {
  filename      = "../lambdas/parser.py.zip"
  function_name = "parser-lambda"
  role          = aws_iam_role.parser_role.arn
  handler       = "parser.lambda_handler"
  runtime       = "python3.8"
  layers        = [aws_lambda_layer_version.lambda-layer.arn, aws_lambda_layer_version.lambda-requests-layer.arn]

  environment {
    variables = {
      foo = "bar"
    }
  }
}

resource "aws_lambda_function" "ai-lambda" {
  filename      = "../lambdas/ai-prediction.py.zip"
  function_name = "prediction-lambda"
  role          = aws_iam_role.ai-prediction_role.arn
  handler       = "ai-prediction.lambda_handler"
  runtime       = "python3.8"
  layers        = [aws_lambda_layer_version.lambda-layer.arn]

  environment {
    variables = {
      foo = "bar"
    }
  }
}

resource "aws_lambda_layer_version" "lambda-layer" {
  filename    = "../lambdas/pandas_layer_v2.zip"
  layer_name  = "pandas3_8"
  description = "Pandas lib for python3.8"

  compatible_runtimes = ["python3.8"]
}

resource "aws_lambda_layer_version" "lambda-requests-layer" {
  filename    = "../lambdas/requests_layer.zip"
  layer_name  = "requests3_8"
  description = "Requests lib for HTTP"

  compatible_runtimes = ["python3.8"]
}

