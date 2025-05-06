variable "name" {
  description = "Name of the monitor"
  type        = string
}

variable "type" {
  description = "Type of the monitor"
  type        = string
  
  validation {
    condition     = contains(["composite", "event alert", "log alert", "metric alert", "process alert", "query alert", "rum alert", "service check", "synthetics alert", "trace-analytics alert", "slo alert"], var.type)
    error_message = "Monitor type must be one of the supported Datadog monitor types."
  }
}

variable "message" {
  description = "Message included with notifications for this monitor"
  type        = string
}

variable "query" {
  description = "Query defines when the monitor triggers"
  type        = string
}

variable "tags" {
  description = "List of tags to associate with the monitor"
  type        = list(string)
  default     = []
}

variable "notify_no_data" {
  description = "Whether to notify when no data is received"
  type        = bool
  default     = false
}

variable "no_data_timeframe" {
  description = "Number of minutes before notifying when no data is received"
  type        = number
  default     = 10
}

variable "notify_audit" {
  description = "Whether to notify on changes to the monitor"
  type        = bool
  default     = false
}

variable "timeout_h" {
  description = "Number of hours of no data after which the monitor will resolve from an alert state"
  type        = number
  default     = 0
}

variable "include_tags" {
  description = "Whether to include triggering tags in notification messages"
  type        = bool
  default     = true
}

variable "require_full_window" {
  description = "Whether the monitor needs a full window of data before evaluating"
  type        = bool
  default     = true
}

variable "renotify_interval" {
  description = "Number of minutes after last notification before re-notifying on alert conditions"
  type        = number
  default     = 0
}

variable "escalation_message" {
  description = "Message to include with re-notifications"
  type        = string
  default     = ""
}

variable "thresholds" {
  description = "Alert thresholds of the monitor"
  type        = map(string)
  default     = null
}

variable "threshold_windows" {
  description = "Mapping of threshold windows used in the monitor"
  type        = map(string)
  default     = null
}