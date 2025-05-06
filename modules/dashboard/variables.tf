variable "title" {
  description = "Title of the dashboard"
  type        = string
}

variable "description" {
  description = "Description of the dashboard"
  type        = string
  default     = ""
}

variable "layout_type" {
  description = "Layout type of the dashboard"
  type        = string
  default     = "ordered"
  
  validation {
    condition     = contains(["ordered", "free"], var.layout_type)
    error_message = "Layout type must be either 'ordered' or 'free'."
  }
}

variable "is_read_only" {
  description = "Whether the dashboard is read-only"
  type        = bool
  default     = false
}

variable "widgets" {
  description = "List of widget configurations for the dashboard"
  type        = any
  default     = []
}

variable "tags" {
  description = "List of tags to associate with the dashboard"
  type        = list(string)
  default     = []
}