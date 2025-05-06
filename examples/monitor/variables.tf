variable "environment" {
  description = "Environment name (prod, staging, dev)"
  type        = string
  default     = "prod"
}

variable "service_name" {
  description = "Name of the service to monitor"
  type        = string
  default     = "api"
}

variable "team" {
  description = "Team responsible for the service"
  type        = string
  default     = "backend"
}

variable "latency_threshold" {
  description = "Critical threshold for service latency in milliseconds"
  type        = string
  default     = "200"
}

variable "latency_recovery_threshold" {
  description = "Recovery threshold for critical service latency in milliseconds"
  type        = string
  default     = "150"
}

variable "latency_warning_threshold" {
  description = "Warning threshold for service latency in milliseconds"
  type        = string
  default     = "150"
}

variable "latency_warning_recovery_threshold" {
  description = "Recovery threshold for warning service latency in milliseconds"
  type        = string
  default     = "100"
}