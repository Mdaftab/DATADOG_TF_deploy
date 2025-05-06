variable "datadog_api_key" {
  type        = string
  description = "Datadog API key"
  sensitive   = true
}

variable "datadog_app_key" {
  type        = string
  description = "Datadog application key"
  sensitive   = true
}

variable "datadog_api_url" {
  type        = string
  description = "Datadog API URL"
  default     = "https://api.datadoghq.com/"
}

variable "environment" {
  type        = string
  description = "Environment to deploy resources into (dev, staging, prod)"
  default     = "dev"
  
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be one of: dev, staging, prod."
  }
}

variable "global_tags" {
  type        = map(string)
  description = "Global tags to apply to all resources"
  default     = {}
}

# Resource definitions - these map to the modules in the /resources directory
variable "dashboards" {
  type        = any
  description = "Map of dashboards to create"
  default     = {}
}

variable "monitors" {
  type        = any
  description = "Map of monitors to create"
  default     = {}
}

variable "log_monitors" {
  type        = any
  description = "Map of log monitors to create"
  default     = {}
}

variable "apm_monitors" {
  type        = any
  description = "Map of APM monitors to create"
  default     = {}
}

variable "host_maps" {
  type        = any
  description = "Map of host maps to create"
  default     = {}
}

variable "container_maps" {
  type        = any
  description = "Map of container maps to create"
  default     = {}
}

variable "metrics_explorers" {
  type        = any
  description = "Map of metrics explorers to create"
  default     = {}
}

variable "synthetics" {
  type        = any
  description = "Map of synthetic tests to create"
  default     = {}
}

variable "service_level_objectives" {
  type        = any
  description = "Map of SLOs to create"
  default     = {}
}