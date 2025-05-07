variable "datadog_api_key" {
  description = "Datadog API key"
  type        = string
  sensitive   = true
}

variable "datadog_app_key" {
  description = "Datadog application key"
  type        = string
  sensitive   = true
}

variable "datadog_api_url" {
  description = "Datadog API URL"
  type        = string
  default     = "https://api.datadoghq.com/"
}

variable "environment" {
  description = "Environment to deploy resources into (prod, staging)"
  type        = string
  
  validation {
    condition     = contains(["prod", "staging"], var.environment)
    error_message = "Environment must be one of: prod, staging"
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