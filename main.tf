# Main Terraform configuration file

terraform {
  required_providers {
    datadog = {
      source  = "DataDog/datadog"
      version = "~> 3.30.0"
    }
  }
  required_version = ">= 1.0.0"
}

provider "datadog" {
  api_key = var.datadog_api_key
  app_key = var.datadog_app_key
  api_url = var.datadog_api_url
}

locals {
  config = yamldecode(file("${path.module}/config/${var.environment}/resources.yaml"))
}

module "monitors" {
  source   = "./modules/monitors"
  monitors = local.config.monitors
}

module "dashboards" {
  source   = "./modules/dashboards"
  dashboards = local.config.dashboards
}

module "slos" {
  source = "./modules/slos"
  slos = local.config.slos
}

# Additional resource types can be added in a similar pattern
# Example of how to add more resource types:
#
# module "new_resource_type" {
#   source   = "./modules/new_resource_type"
#   resources = local.config.new_resource_type
# }
