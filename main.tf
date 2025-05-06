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
  # Format global tags as a list
  global_tags_list = [for k, v in var.global_tags : "${k}:${v}"]
  
  # Add environment tag to global tags
  common_tags = concat(local.global_tags_list, ["env:${var.environment}"])
  
  # Default values for common properties
  defaults = {
    environment = var.environment
  }
}

# Dashboards
module "dashboards" {
  source   = "./modules/dashboard"
  for_each = var.dashboards

  # Common parameters
  title       = each.value.title
  description = lookup(each.value, "description", "")
  layout_type = lookup(each.value, "layout_type", "ordered")
  is_read_only = lookup(each.value, "is_read_only", false)
  
  # Dashboard-specific parameters
  widgets = lookup(each.value, "widgets", [])
  
  # Merge global tags with resource-specific tags
  tags = concat(local.common_tags, lookup(each.value, "tags", []))
}

# Monitors
module "monitors" {
  source   = "./modules/monitor"
  for_each = var.monitors

  # Common parameters
  name    = each.value.name
  type    = each.value.type
  message = each.value.message
  query   = each.value.query
  
  # Alert options
  notify_no_data     = lookup(each.value, "notify_no_data", false)
  no_data_timeframe  = lookup(each.value, "no_data_timeframe", 10)
  notify_audit       = lookup(each.value, "notify_audit", false)
  timeout_h          = lookup(each.value, "timeout_h", 0)
  include_tags       = lookup(each.value, "include_tags", true)
  require_full_window = lookup(each.value, "require_full_window", true)
  renotify_interval  = lookup(each.value, "renotify_interval", 0)
  escalation_message = lookup(each.value, "escalation_message", "")
  
  # Thresholds
  thresholds = lookup(each.value, "thresholds", null)
  threshold_windows = lookup(each.value, "threshold_windows", null)
  
  # Merge global tags with resource-specific tags
  tags = concat(local.common_tags, lookup(each.value, "tags", []))
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