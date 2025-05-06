# Datadog Terraform Deployment

This project contains Terraform modules and templates for deploying Datadog resources following best practices.

## Project Overview

This repository provides a structured approach to deploying Datadog monitoring resources, including:

- Dashboards
- Monitors (Alerts)
- Log Monitors
- APM Monitors
- Infrastructure Lists
- Host Maps
- Container Maps
- Metrics Explorers
- Events Streams
- And more observability modules

## Key Features

- **Modular Design**: Reusable Terraform modules for each Datadog resource type
- **Simple Developer Experience**: Templates with clear examples for each resource
- **Consistent Structure**: Standardized approach to resource configuration
- **Best Practices**: Built-in conventions for naming, tagging, and organization

## Getting Started

### Prerequisites

- Terraform ≥ 1.0.0
- Datadog API and Application keys
- Basic understanding of Terraform and Datadog concepts

### Setup

1. Clone this repository
2. Create a `terraform.tfvars` file with your Datadog credentials:

```hcl
datadog_api_key = "your_api_key"
datadog_app_key = "your_app_key"
```

3. Initialize Terraform:

```bash
terraform init
```

## Usage

### For DevOps Teams

DevOps teams can maintain and extend the templates:

1. Develop new modules in the `modules/` directory
2. Create examples in the `examples/` directory
3. Document modules in their respective README files

See [How to Create New Module](docs/HOW_TO_CREATE_NEW_MODULE.md) for detailed instructions.

### For Developers

Developers can deploy resources by:

1. Copying an example configuration
2. Customizing the variables to match their requirements
3. Deploying using standard Terraform commands

See [Usage Guide](docs/USAGE_GUIDE.md) for detailed instructions.

## Project Structure

```
.
├── modules/               # Reusable Terraform modules for each resource type
├── examples/              # Example implementations for each module
├── environments/          # Environment-specific configurations
├── templates/             # Templates for creating new modules
├── docs/                  # Documentation
└── scripts/               # Utility scripts
```

## Available Modules

- **Dashboard**: Create customizable Datadog dashboards
- **Monitor**: Create and manage Datadog monitors
- **Log Monitor**: Create specialized log-based monitors
- **APM Monitor**: Monitor application performance metrics
- *(Additional modules will be added as needed)*

## Deployment Process

The typical process for deploying a new Datadog resource:

1. Find the appropriate module example
2. Copy and customize the example configuration
3. Run Terraform to deploy your resource:

```bash
# Initialize Terraform
terraform init

# Review changes
terraform plan

# Apply changes
terraform apply
```

## Best Practices

- Use consistent tagging for all resources
- Follow the established naming conventions
- Document the purpose of each resource
- Organize resources by environment and team

## Contributing

1. Create a new branch for your changes
2. Follow the established module structure
3. Include examples for your changes
4. Update documentation as needed
5. Submit a pull request

## Documentation

- [Usage Guide](docs/USAGE_GUIDE.md)
- [How to Create New Module](docs/HOW_TO_CREATE_NEW_MODULE.md)