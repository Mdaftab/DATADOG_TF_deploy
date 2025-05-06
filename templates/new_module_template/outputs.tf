output "resource_id" {
  description = "ID of the created resource"
  value       = datadog_RESOURCE_TYPE.this.id
}

output "resource_name" {
  description = "Name of the created resource"
  value       = datadog_RESOURCE_TYPE.this.name
}

# Add additional outputs specific to the resource type
# output "resource_specific_output" {
#   description = "Description of the specific output"
#   value       = datadog_RESOURCE_TYPE.this.specific_attribute
# }