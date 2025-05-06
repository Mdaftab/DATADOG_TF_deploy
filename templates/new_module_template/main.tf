# Module template - main configuration

# Replace "resource_type" with the actual Datadog resource type you're creating
resource "datadog_RESOURCE_TYPE" "this" {
  # Required parameters
  name        = var.name
  
  # Common optional parameters with defaults
  description = var.description
  
  # Resource-specific parameters to be customized
  # parameter1 = var.parameter1
  # parameter2 = var.parameter2
  
  # Tags for resource tracking and organization
  tags = var.tags
}