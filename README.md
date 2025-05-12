# Datadog Terraform Deployment Skeleton

This project provides a best-practice skeleton for deploying Datadog resources using Terraform. It's designed for DevOps and SRE professionals to quickly set up and extend Datadog monitoring and dashboards in their environments.

## Project Goal

To offer a clear, modular, and easy-to-use foundation for managing Datadog resources with Terraform, promoting best practices and enabling teams to customize and expand for their specific needs.

## Key Features

- **Modular Terraform:** Organized modules for different Datadog resource types.
- **Environment Support:** Easily manage configurations for multiple environments (dev, staging, prod).
- **CLI Tooling:** Helper scripts for common tasks like creating resource configurations.
- **Best Practices:** Designed with recommended Datadog and Terraform practices in mind.

## Getting Started: A Step-by-Step Guide

Follow these steps to set up and use this project:

### Step 1: Clone the Repository

Start by cloning the project to your local machine:

```bash
git clone https://github.com/yourusername/datadog-tf-deploy.git
cd datadog-tf-deploy
```

### Step 2: Install Prerequisites

Ensure you have the necessary tools installed:

-   **Terraform:** Install Terraform (version 1.0.0 or later). Follow the official [Terraform installation guide](https://developer.hashicorp.com/terraform/downloads).
-   **Python 3.6+:** Install Python 3.6 or later.
-   **Python Dependencies:** Install the required Python packages for the CLI tool:
    ```bash
    pip install click pyyaml
    ```

### Step 3: Configure Datadog Credentials

You need to provide your Datadog API and Application keys.

1.  Copy the example Terraform variables file:
    ```bash
    cp terraform.tfvars.example terraform.tfvars
    ```
2.  Edit `terraform.tfvars` and replace the placeholder values with your actual Datadog keys and API URL:
    ```hcl
    datadog_api_key = "your_api_key_here"
    datadog_app_key = "your_app_key_here"
    datadog_api_url = "https://api.datadoghq.com/" # Or your specific Datadog site URL
    ```
    **Note:** Treat your API and App keys as sensitive information. Do not commit `terraform.tfvars` to version control if it contains secrets. Use a secrets management system or environment variables in production.

### Step 4: Initialize Terraform

Navigate to the project root directory and initialize Terraform. This downloads the necessary provider plugins.

```bash
terraform init
```

### Step 5: Define Your Datadog Resources

Resource configurations are defined in `.tfvars` files, typically organized by environment in the `environments/` directory.

1.  Choose an environment (e.g., `dev` or `prod`).
2.  Edit the corresponding `terraform.tfvars` file (e.g., `environments/dev/terraform.tfvars`).
3.  Define your Datadog resources (monitors, dashboards, SLOs, etc.) using the variables provided by the modules. Refer to the examples in the `examples/` directory and the module documentation for structure and available parameters.

    Example snippet from `environments/dev/terraform.tfvars`:
    ```hcl
    environment = "dev"

    global_tags = {
      managed_by = "terraform"
      team       = "platform"
      env        = "dev"
    }

    monitors = {
      api_latency = {
        name    = "DEV - High API Latency"
        type    = "metric alert"
        message = "Service latency is above threshold in dev. @slack-dev-alerts"
        query   = "avg(last_5m):avg:service.latency{env:dev,service:api} > 500"
        thresholds = {
          critical          = "500"
          critical_recovery = "400"
        }
        notify_no_data = false
        tags = ["service:api"]
      }
    }

    dashboards = {
      service_overview = {
        title       = "DEV - Service Overview Dashboard"
        description = "Key metrics for our service in development"
        widgets = [
          {
            definition_type = "timeseries"
            title = "Service Latency"
            request = {
              query = "avg:service.latency{env:dev} by {service}"
              display_type = "line"
            }
            markers = [
              {
                display_type = "error dashed"
                value = "500"
                label = "SLA Threshold"
              }
            ]
          }
        ]
        tags = ["service:api"]
      }
    }
    ```

### Step 6: Validate Your Configuration

Before deploying, validate your Terraform configuration:

```bash
terraform validate
```

This checks for syntax errors and consistency.

### Step 7: Preview Changes (Terraform Plan)

Generate a plan to see what actions Terraform will take without applying them:

```bash
terraform plan -var-file=environments/dev/terraform.tfvars
```

Replace `environments/dev/terraform.tfvars` with the path to your environment's tfvars file. Review the output carefully to understand the proposed changes.

### Step 8: Deploy Resources (Terraform Apply)

If the plan looks correct, apply the changes to deploy your Datadog resources:

```bash
terraform apply -var-file=environments/dev/terraform.tfvars
```

Again, replace with your environment's tfvars file. Terraform will prompt for confirmation before proceeding (unless you use `-auto-approve`).

## Project Structure

```shell
project/
├── modules/                    # Reusable Terraform modules for Datadog resources
│   ├── single_monitor/        # Module for creating a single Datadog monitor
│   ├── multiple_monitors/     # Module for creating multiple Datadog monitors from a map
│   ├── dashboard/             # Module for creating Datadog dashboards
│   └── slos/                  # Module for creating Datadog SLOs
├── environments/              # Environment-specific variable definitions
│   ├── dev/                   # Development environment variables
│   │   └── terraform.tfvars
│   └── prod/                  # Production environment variables
│       └── terraform.tfvars
├── examples/                  # Example configurations using the modules
│   ├── templates/             # Pre-defined YAML templates (used by CLI tool)
│   │   ├── api-monitoring.yaml
│   │   └── database-monitoring.yaml
│   │   └── microservice-monitoring.yaml
│   ├── dashboard/             # Example of using the dashboard module
│   └── monitor/               # Example of using the single_monitor module
├── scripts/                   # Helper scripts
│   ├── create-resource.sh     # Script to help create new resource configurations
│   └── datadog-tf-cli.py      # CLI tool for template generation, validation, etc.
├── docs/                      # Project documentation
│   ├── HOW_TO_CREATE_NEW_MODULE.md # Guide for adding new module types
│   └── USAGE_GUIDE.md         # Detailed usage instructions
├── main.tf                    # Main Terraform configuration, references modules
├── variables.tf               # Global input variables for the root module
├── terraform.tfvars.example   # Example for root-level variables (like API keys)
└── .gitignore                 # Specifies intentionally untracked files
```

## Extending the Project

-   **Add a New Resource Type:** Follow the guide in `docs/HOW_TO_CREATE_NEW_MODULE.md` to create a new module and integrate it.
-   **Create New Examples/Templates:** Add examples in the `examples/` directory to demonstrate new patterns or resource types.
-   **Enhance CLI Tool:** Modify scripts in `scripts/` to add new functionality.

## Best Practices

Refer to the `.clinerules/datadog-terraform-best-practices.md` file for detailed guidelines on naming conventions, tagging, variable usage, and more.

## Contributing

Contributions are welcome! Please refer to the `CONTRIBUTING.md` file (if it exists) or the general guidelines for contributing to open-source projects.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
