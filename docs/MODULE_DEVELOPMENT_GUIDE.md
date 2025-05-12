# Module Development Guide

This guide provides detailed instructions for creating new modules in the Datadog Terraform Deployment project. It's designed for DevOps and SRE professionals who want to extend the project with additional Datadog resource types.

## Table of Contents

- [Module Structure](#module-structure)
- [Development Workflow](#development-workflow)
- [Best Practices](#best-practices)
- [Testing Your Module](#testing-your-module)
- [Documentation](#documentation)
- [Examples](#examples)

## Module Structure

Each module should follow this standard structure:

```
modules/
└── your_module_name/
    ├── main.tf           # Main Terraform configuration
    ├── variables.tf      # Input variables
    ├── outputs.tf        # Output values
    ├── README.md         # Module documentation
    └── templates/        # Optional templates directory
        └── message.tpl   # Message templates
```

### main.tf

The `main.tf` file contains the Terraform resource definitions. It should:

- Use variables for all configurable parameters
- Include proper resource naming
- Use dynamic blocks for complex nested structures
- Include proper tagging

Example:

```hcl
resource "datadog_monitor" "monitor" {
  name               = var.name
  type               = var.type
  message            = var.message
  query              = var.query
  
  # Alert options
  notify_no_data     = var.notify_no_data
  no_data_timeframe  = var.notify_no_data ? var.no_data_timeframe : null
  
  # Thresholds
  dynamic "thresholds" {
    for_each = var.thresholds != null ? [1] : []
    content {
      ok                = lookup(var.thresholds, "ok", null)
      warning           = lookup(var.thresholds, "warning", null)
      critical          = lookup(var.thresholds, "critical", null)
    }
  }
  
  tags = var.tags
}
```

### variables.tf

The `variables.tf` file defines all input variables for the module. It should:

- Include proper descriptions for all variables
- Set default values where appropriate
- Include validation rules
- Group related variables with comments

Example:

```hcl
variable "name" {
  description = "Name of the resource"
  type        = string
}

variable "type" {
  description = "Type of the resource"
  type        = string
  
  validation {
    condition     = contains(["metric alert", "log alert"], var.type)
    error_message = "Type must be one of the supported types."
  }
}

# Alert options
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

# Tags
variable "tags" {
  description = "List of tags to associate with the resource"
  type        = list(string)
  default     = []
}
```

### outputs.tf

The `outputs.tf` file defines the outputs from the module. It should:

- Include the resource ID
- Include any useful attributes
- Include URLs to view the resource in the Datadog UI

Example:

```hcl
output "id" {
  description = "The ID of the created resource"
  value       = datadog_monitor.monitor.id
}

output "name" {
  description = "The name of the created resource"
  value       = datadog_monitor.monitor.name
}

output "url" {
  description = "The URL to view the resource in Datadog"
  value       = "https://app.datadoghq.com/monitors/${datadog_monitor.monitor.id}"
}
```

### README.md

The `README.md` file provides documentation for the module. It should include:

- Description of the module
- Usage examples
- Input variables documentation
- Output values documentation
- Any special considerations

## Development Workflow

Follow these steps to create a new module:

1. **Identify the Resource Type**

   Determine which Datadog resource type you want to support. Check the [Datadog Terraform Provider documentation](https://registry.terraform.io/providers/DataDog/datadog/latest/docs) for available resource types.

2. **Create the Module Structure**

   ```bash
   mkdir -p modules/your_module_name
   touch modules/your_module_name/{main.tf,variables.tf,outputs.tf,README.md}
   ```

3. **Implement the Module**

   - Define the resource in `main.tf`
   - Define variables in `variables.tf`
   - Define outputs in `outputs.tf`
   - Document the module in `README.md`

4. **Create Examples**

   ```bash
   mkdir -p examples/your_module_name
   touch examples/your_module_name/{main.tf,variables.tf,outputs.tf,README.md}
   ```

5. **Create Templates**

   Add YAML templates in `examples/templates/your-template.yaml`

6. **Test the Module**

   Test the module using the examples you created.

7. **Update Documentation**

   Update the main project documentation to include your new module.

## Best Practices

### Resource Naming

Use consistent naming patterns for all resources:

```
[env]-[team]-[service]-[resource-type]
```

### Variable Validation

Include validation rules for all input parameters:

```hcl
variable "threshold" {
  description = "Alert threshold value"
  type        = number
  
  validation {
    condition     = var.threshold > 0
    error_message = "Threshold must be greater than 0."
  }
}
```

### Dynamic Blocks

Use dynamic blocks for complex nested structures:

```hcl
dynamic "thresholds" {
  for_each = var.thresholds != null ? [1] : []
  content {
    ok                = lookup(var.thresholds, "ok", null)
    warning           = lookup(var.thresholds, "warning", null)
    critical          = lookup(var.thresholds, "critical", null)
  }
}
```

### Tagging

Always include proper tagging:

```hcl
tags = concat(
  var.tags,
  [
    "env:${var.environment}",
    "service:${var.service_name}",
    "team:${var.team}"
  ]
)
```

## Testing Your Module

1. **Create a Test Configuration**

   Create a test configuration in the `examples` directory.

2. **Initialize Terraform**

   ```bash
   cd examples/your_module_name
   terraform init
   ```

3. **Validate the Configuration**

   ```bash
   terraform validate
   ```

4. **Plan the Changes**

   ```bash
   terraform plan
   ```

5. **Apply the Changes**

   ```bash
   terraform apply
   ```

6. **Verify the Resources**

   Verify that the resources were created correctly in the Datadog UI.

## Documentation

### Module Documentation

Each module should have a README.md file with:

- Description of the module
- Usage examples
- Input variables documentation
- Output values documentation

Example:

```markdown
# Datadog Monitor Module

This module creates Datadog monitors with standardized configuration.

## Usage

```hcl
module "api_latency_monitor" {
  source = "../../modules/monitor"

  name  = "API Latency Monitor"
  type  = "metric alert"
  query = "avg(last_5m):avg:trace.http.request.duration{service:api} > 1000"
  
  message = <<-EOT
    API latency is above threshold.
    
    @slack-alerts @pagerduty
  EOT
  
  tags = ["service:api", "env:prod"]
}
```

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| name | Name of the monitor | `string` | n/a | yes |
| type | Type of the monitor | `string` | n/a | yes |
| query | Query defines when the monitor triggers | `string` | n/a | yes |
| message | Message included with notifications | `string` | n/a | yes |
| tags | List of tags to associate with the monitor | `list(string)` | `[]` | no |

## Outputs

| Name | Description |
|------|-------------|
| id | The ID of the created monitor |
| name | The name of the created monitor |
| url | The URL to view the monitor in Datadog |
```

### Example Documentation

Each example should have a README.md file with:

- Description of the example
- Usage instructions
- Expected outcome

## Examples

### Basic Example

```hcl
module "api_latency_monitor" {
  source = "../../modules/monitor"

  name  = "API Latency Monitor"
  type  = "metric alert"
  query = "avg(last_5m):avg:trace.http.request.duration{service:api} > 1000"
  
  message = "API latency is above threshold."
  
  tags = ["service:api", "env:prod"]
}
```

### Complex Example

```hcl
module "api_latency_monitor" {
  source = "../../modules/monitor"

  name  = "API Latency Monitor"
  type  = "metric alert"
  query = "avg(last_5m):avg:trace.http.request.duration{service:api} > ${var.latency_threshold}"
  
  message = templatefile("${path.module}/templates/alert_message.tpl", {
    service = "API",
    threshold = var.latency_threshold,
    runbook_url = "https://wiki.example.com/runbooks/api-latency"
  })
  
  thresholds = {
    critical = var.latency_threshold,
    warning = var.latency_threshold * 0.8
  }
  
  notify_no_data = true
  no_data_timeframe = 10
  
  tags = concat(
    var.tags,
    [
      "service:api",
      "env:${var.environment}",
      "team:${var.team}"
    ]
  )
}
```

By following this guide, you'll create modules that are consistent, well-documented, and easy to use by other team members.
