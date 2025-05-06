variable "name" {
  description = "Name of the resource"
  type        = string
}

variable "description" {
  description = "Description of the resource"
  type        = string
  default     = ""
}

# Example of a variable with validation
# variable "parameter1" {
#   description = "Description of parameter1"
#   type        = string
#   
#   validation {
#     condition     = length(var.parameter1) > 0
#     error_message = "Parameter1 cannot be empty."
#   }
# }

# Example of a complex type variable
# variable "parameter2" {
#   description = "Description of parameter2"
#   type        = map(string)
#   default     = {}
# }

variable "tags" {
  description = "List of tags to associate with the resource"
  type        = list(string)
  default     = []
}