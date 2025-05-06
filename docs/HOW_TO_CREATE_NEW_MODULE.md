# How to Create a New Datadog Module

This guide walks through the process of creating a new module for a Datadog resource type.

## Step 1: Start with the Template

Copy the template directory to create a new module:

```bash
cp -r templates/new_module_template modules/your_module_name
```

## Step 2: Update the Resource Type

In `main.tf`, replace `datadog_RESOURCE_TYPE` with the appropriate Datadog resource, such as:
- `datadog_dashboard`
- `datadog_monitor`
- `datadog_synthetics_test`
- `datadog_service_level_objective`
- `datadog_logs_custom_pipeline`

## Step 3: Define Required Parameters

Update `variables.tf` with:
- Required parameters for the resource
- Optional parameters with sensible defaults
- Validation rules for parameters
- Descriptions for all variables

## Step 4: Define Outputs

Update `outputs.tf` with:
- Essential resource identifiers (id, name)
- Any useful resource-specific outputs
- Links or URLs to view the resource in Datadog UI

## Step 5: Write Documentation

Update `README.md` with:
- Description of the module
- Usage examples
- Complete input/output documentation
- Resource-specific information
- Common configurations or patterns

## Step 6: Create Example Configuration

Create an example in the `examples` directory:

```bash
mkdir -p examples/your_module_name
```

Create example files:
- `main.tf` - Example module usage
- `variables.tf` - Variables with default values
- `outputs.tf` - Example outputs
- `README.md` - Documentation specific to the example

## Step 7: Test the Module

Test the module with the example configuration:

```bash
cd examples/your_module_name
terraform init
terraform validate
terraform plan
```

## Step 8: Add to CLAUDE.md

Update the CLAUDE.md file to document the new module:

```markdown
## modules/your_module_name

This module provides a template for deploying {resource type} in Datadog.

Commands:
- `terraform apply -var-file=values.tfvars` - Deploy the resource
```

## Tips for Specific Resource Types

### Dashboards
- Use dynamic blocks for widgets
- Consider templating for repeated elements
- Allow for flexible layout configurations

### Monitors
- Include sensible defaults for thresholds
- Provide templates for common notification messages
- Include examples of different evaluation types

### Synthetics Tests
- Include assertion examples
- Document step configurations
- Include location strategy guidance

### SLOs
- Document different SLI types
- Include target and window configurations
- Show examples of different time windows