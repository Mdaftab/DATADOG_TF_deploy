# Datadog Terraform Deployment Usage Guide

This guide explains how to use the Datadog Terraform Deployment Skeleton project to deploy Datadog resources using Terraform.

## Prerequisites

-   Terraform ≥ 1.0.0
-   Python 3.6+ (for the CLI tool)
-   Datadog API and App keys with necessary permissions to create resources.

## Getting Started

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd DATADOG_TF_deploy
    ```

2.  **Install Python dependencies:**
    ```bash
    pip install click pyyaml
    ```

3.  **Configure Datadog credentials:**
    Copy the example variables file and add your Datadog API and App keys.
    ```bash
    cp terraform.tfvars.example terraform.tfvars
    ```
    Edit `terraform.tfvars`:
    ```hcl
    datadog_api_key = "your_api_key_here"
    datadog_app_key = "your_app_key_here"
    datadog_api_url = "https://api.datadoghq.com/" # Or your specific Datadog site URL
    ```
    **Note:** Do not commit `terraform.tfvars` with secrets to version control.

4.  **Initialize Terraform:**
    ```bash
    terraform init
    ```

## Defining and Deploying Resources

Resource configurations are defined in environment-specific `.tfvars` files located in the `environments/` directory.

1.  **Choose your environment:** Navigate to the `environments/` directory and select the `.tfvars` file for your target environment (e.g., `dev/terraform.tfvars`, `prod/terraform.tfvars`).

2.  **Define your resources:** Edit the environment's `terraform.tfvars` file to define the Datadog resources you want to deploy. Use the variables provided by the modules in the `modules/` directory. Refer to the examples in `examples/` for guidance on the structure for defining monitors, dashboards, SLOs, etc.

    Example structure within an environment's `terraform.tfvars`:
    ```hcl
    environment = "dev" # Or prod, staging

    global_tags = {
      managed_by = "terraform"
      team       = "your-team"
      env        = var.environment
    }

    monitors = {
      # Define multiple monitors here using the 'multiple_monitors' module
      my_service_cpu_alert = {
        name      = "${var.environment}-my-service-high-cpu"
        type      = "metric alert"
        query     = "avg(last_5m):avg:system.cpu.user{service:my-service,env:${var.environment}} > 80"
        message   = "High CPU usage for my-service in ${var.environment}. @slack-channel"
        threshold = 80
        tags      = ["service:my-service", "env:${var.environment}", "team:your-team"]
      }
      # Add more monitor definitions...
    }

    dashboards = {
      # Define dashboards here using the 'dashboard' module
      my_service_overview = {
        title       = "${var.environment} - My Service Overview"
        description = "Overview dashboard for my-service in ${var.environment}"
        # ... dashboard widget definitions ...
        tags = ["service:my-service", "env:${var.environment}", "team:your-team"]
      }
      # Add more dashboard definitions...
    }

    service_level_objectives = {
      # Define SLOs here using the 'slos' module
      my_service_availability = {
        name      = "${var.environment} - My Service Availability SLO"
        target    = 99.9
        timeframe = "30d"
        # ... SLO query definition ...
        tags = ["service:my-service", "env:${var.environment}", "team:your-team"]
      }
      # Add more SLO definitions...
    }

    # Add definitions for other resource types (synthetics, etc.) as needed
    ```

3.  **Validate your configuration:**
    ```bash
    terraform validate -var-file=environments/dev/terraform.tfvars
    ```
    Replace `environments/dev/terraform.tfvars` with the path to your environment's tfvars file.

4.  **Preview changes (Terraform Plan):**
    ```bash
    terraform plan -var-file=environments/dev/terraform.tfvars
    ```
    Review the output to understand what resources will be created, updated, or deleted.

5.  **Deploy resources (Terraform Apply):**
    ```bash
    terraform apply -var-file=environments/dev/terraform.tfvars
    ```
    Confirm the changes when prompted.

## Using the CLI Tool

The `scripts/datadog-tf-cli.py` tool provides helper commands:

-   **Generate a template:**
    ```bash
    python scripts/datadog-tf-cli.py template <resource_type> <output_file> [--template <specialized_template>]
    # Example: Generate a basic monitor template
    python scripts/datadog-tf-cli.py template monitor my-new-monitor.yaml
    # Example: Generate a microservice monitoring template
    python scripts/datadog-tf-cli.py template specialized microservice-config.yaml --template microservice-monitoring
    ```
    Use `python scripts/datadog-tf-cli.py list` to see available templates.

-   **Validate a configuration file:**
    ```bash
    python scripts/datadog-tf-cli.py validate <config_file>
    ```

-   **Preview changes for a configuration file:**
    ```bash
    python scripts/datadog-tf-cli.py plan <config_file>
    ```

-   **Apply a configuration file:**
    ```bash
    python scripts/datadog-tf-cli.py apply <config_file> [--auto-approve]
    ```

## Extending the Project

Refer to `docs/HOW_TO_CREATE_NEW_MODULE.md` for detailed instructions on adding support for new Datadog resource types by creating new Terraform modules.

## Best Practices

Consult the `.clinerules/datadog-terraform-best-practices.md` file for guidelines on naming, tagging, and other recommended practices.
