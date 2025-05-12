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

module "multiple_monitors" {
  source   = "./modules/multiple_monitors"
  monitors = var.monitors
}

module "dashboards" {
  source   = "./modules/dashboards"
  dashboards = var.dashboards
}

module "slos" {
  source = "./modules/slos"
  slos = var.service_level_objectives
}

# Additional resource types can be added in a similar pattern
# Example of how to add more resource types:
#
# module "new_resource_type" {
#   source   = "./modules/new_resource_type"
#   resources = var.new_resource_type
# }
