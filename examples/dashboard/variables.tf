# Example dashboard variables
# These would be used for environment-specific configurations

variable "environment" {
  description = "Environment name (prod, staging, dev)"
  type        = string
  default     = "prod"
}

variable "service_name" {
  description = "Name of the service for which the dashboard is created"
  type        = string
  default     = "api"
}

variable "team" {
  description = "Team responsible for the service"
  type        = string
  default     = "backend"
}