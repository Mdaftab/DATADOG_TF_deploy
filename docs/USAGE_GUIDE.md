# Datadog Terraform Deployment Guide

This guide explains how to use this repository to deploy Datadog resources using Terraform.

## Prerequisites

- Terraform ≥ 1.0.0
- Datadog API and App keys
- Proper IAM permissions to deploy resources

## Getting Started

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd DATADOG_TF_deploy
   ```

2. Create a `terraform.tfvars` file with your Datadog API credentials:
   ```hcl
   datadog_api_key = "your-api-key"
   datadog_app_key = "your-app-key"
   datadog_api_url = "https://api.datadoghq.com/" # or your specific Datadog site URL
   ```

3. Initialize Terraform:
   ```bash
   terraform init
   ```

## Deploying Resources

### Using Modules Directly

You can use modules directly in your Terraform configuration:

```hcl
module "service_dashboard" {
  source = "./modules/dashboard"

  title       = "My Service Dashboard"
  description = "Dashboard for my service"
  
  # Additional module-specific parameters
}
```

### Using Examples as Templates

Each module includes examples that you can copy and modify:

1. Copy an example directory:
   ```bash
   cp -r examples/dashboard my-dashboard
   ```

2. Modify the variables and configurations in the copied directory:
   ```bash
   cd my-dashboard
   # Edit variables.tf and main.tf to customize
   ```

3. Initialize and deploy:
   ```bash
   terraform init
   terraform plan
   terraform apply
   ```

## Developer Workflow

The typical workflow for a developer to deploy a new Datadog resource is:

1. Find the appropriate module for the resource type (dashboard, monitor, etc.)
2. Copy the example for that module to a new directory
3. Modify the variables to match your requirements
4. Deploy using Terraform

## Using Environment-Specific Configurations

For different environments (dev, staging, prod):

1. Create environment-specific variable files:
   ```bash
   # dev.tfvars
   environment = "dev"
   team = "backend"
   ```

2. Apply with the specific environment:
   ```bash
   terraform apply -var-file=dev.tfvars
   ```

## Extending the Project

To add support for a new Datadog resource type:

1. Follow the guidelines in `docs/HOW_TO_CREATE_NEW_MODULE.md`
2. Create a new module in the `modules/` directory
3. Create examples in the `examples/` directory
4. Update documentation as needed

## Best Practices

1. **Use Tags Consistently**
   ```hcl
   tags = [
     "team:${var.team}",
     "service:${var.service_name}",
     "env:${var.environment}"
   ]
   ```

2. **Version Resources**
   Consider adding a version tag to resources to track changes.

3. **Document Resource Purpose**
   Always include a meaningful description for each resource.

4. **Use Variables for Repeated Values**
   Extract common values like environment and team names to variables.

5. **Follow Naming Conventions**
   Use consistent naming patterns for all resources:
   ```
   [env]-[team]-[service]-[resource-type]
   ```

## Common Operations

### Creating a New Dashboard

```bash
# Copy the example
cp -r examples/dashboard my-new-dashboard

# Customize the configuration
cd my-new-dashboard
# Edit main.tf and variables.tf

# Deploy
terraform init
terraform apply
```

### Creating a New Monitor

```bash
# Copy the example
cp -r examples/monitor my-new-monitor

# Customize the configuration
cd my-new-monitor
# Edit main.tf and variables.tf

# Deploy
terraform init
terraform apply
```