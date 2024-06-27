locals {
  demobuilder_fname    = "${var.unique_identifier}_lambda_demobuilder"
  demobuilder_loggroup = "/aws/lambda/${local.demobuilder_fname}"
}

provider "aws" {
  region = var.aws_region
}

provider "archive" {}
