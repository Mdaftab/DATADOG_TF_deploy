# Datadog MODULE_NAME Module

This module creates a customizable Datadog MODULE_NAME.

## Usage

```hcl
module "MODULE_NAME" {
  source = "../../modules/MODULE_NAME"

  name        = "My Resource Name"
  description = "Description of the resource"
  
  # Resource-specific parameters
  parameter1  = "value1"
  parameter2  = {
    key1 = "value1"
    key2 = "value2"
  }
  
  tags = ["team:devops", "environment:prod", "application:my-app"]
}
```

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|----------|
| name | Name of the resource | string | n/a | yes |
| description | Description of the resource | string | "" | no |
| parameter1 | Description of parameter1 | string | n/a | yes |
| parameter2 | Description of parameter2 | map(string) | {} | no |
| tags | List of tags to associate with the resource | list(string) | [] | no |

## Outputs

| Name | Description |
|------|-------------|
| resource_id | ID of the created resource |
| resource_name | Name of the created resource |
| resource_specific_output | Description of the specific output |

## Resource-Specific Information

Add any resource-specific information, guidelines, or constraints here.

## Example Configurations

### Example 1: Basic Usage

```hcl
module "basic_MODULE_NAME" {
  source = "../../modules/MODULE_NAME"

  name        = "Basic Resource"
  description = "Basic configuration for the resource"
  
  tags = ["environment:dev"]
}
```

### Example 2: Advanced Usage

```hcl
module "advanced_MODULE_NAME" {
  source = "../../modules/MODULE_NAME"

  name        = "Advanced Resource"
  description = "Advanced configuration for the resource"
  
  parameter1  = "custom_value"
  parameter2  = {
    advanced_key1 = "advanced_value1"
    advanced_key2 = "advanced_value2"
  }
  
  tags = ["team:devops", "environment:prod", "application:my-app"]
}
```