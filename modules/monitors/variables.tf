variable "monitors" {
  description = "Map of monitors to create"
  type = map(object({
    name        = string
    threshold   = number
    query       = optional(string)
    tags        = list(string)
    notify_no_data = optional(bool)
    no_data_timeframe = optional(number)
    include_tags = optional(bool)
    require_full_window = optional(bool)
    renotify_interval = optional(number)
  }))

  validation {
    condition     = alltrue([for m in var.monitors : m.threshold > 0 && m.threshold <= 100])
    error_message = "Threshold must be between 0 and 100"
  }

  validation {
    condition     = alltrue([for m in var.monitors : length(m.tags) > 0])
    error_message = "At least one tag is required"
  }
} 