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
# Log Monitors
module "log_monitors" {
  source   = "./modules/log_monitor"
  for_each = var.log_monitors

  # These would need to match the module's variables
  # Common parameters here
  
  # Merge global tags with resource-specific tags
  tags = concat(local.common_tags, lookup(each.value, "tags", []))
}

# APM Monitors
module "apm_monitors" {
  source   = "./modules/apm_monitor"
  for_each = var.apm_monitors

  # These would need to match the module's variables
  # Common parameters here
  
  # Merge global tags with resource-specific tags
  tags = concat(local.common_tags, lookup(each.value, "tags", []))
}