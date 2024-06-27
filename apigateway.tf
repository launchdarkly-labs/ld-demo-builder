resource "aws_apigatewayv2_api" "demobuilder_apigw_endpoint" {
  name          = "${var.unique_identifier}_DemoBuilderEndPoint"
  description   = "Lambda DemoBuilder Endpoint"
  protocol_type = "HTTP"
  cors_configuration {
    allow_origins = ["*"]
    allow_methods = ["POST", "GET", "OPTIONS"]
    allow_headers = ["*"]
    max_age       = 300
  }
}

resource "aws_apigatewayv2_stage" "demobuilder_apigw_stage" {
  api_id      = aws_apigatewayv2_api.demobuilder_apigw_endpoint.id
  name        = "builder"
  auto_deploy = true
}

resource "aws_apigatewayv2_integration" "demobuilder_apigw_integration" {
  depends_on = [aws_lambda_function.lambda_demobuilder]

  api_id           = aws_apigatewayv2_api.demobuilder_apigw_endpoint.id
  integration_type = "AWS_PROXY"

  connection_type        = "INTERNET"
  integration_method     = "POST"
  integration_uri        = aws_lambda_function.lambda_demobuilder.invoke_arn
  payload_format_version = "2.0"
  passthrough_behavior   = "WHEN_NO_MATCH"
}

resource "aws_apigatewayv2_route" "demobuilder_apigw_route" {
  api_id             = aws_apigatewayv2_api.demobuilder_apigw_endpoint.id
  route_key          = "$default"
  authorization_type = "NONE"
  target             = "integrations/${aws_apigatewayv2_integration.demobuilder_apigw_integration.id}"
}

resource "aws_lambda_permission" "api_gateway_demobuilder_perms" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_demobuilder.function_name
  principal     = "apigateway.amazonaws.com"

  # The /*/* portion grants access from any method on any resource
  # within the API Gateway "REST API".
  source_arn = "${aws_apigatewayv2_api.demobuilder_apigw_endpoint.execution_arn}/*/*"
}
