# How to Create a New Datadog Module

This guide walks through the process of creating a new module for a Datadog resource type in this project skeleton.

## Module Structure

Each new module should follow this standard structure:

```
modules/
└── your_module_name/
    ├── main.tf           # Main Terraform configuration for the resource
    ├── variables.tf      # Input variables for the module
    ├── outputs.tf        # Output values from the module
    ├── README.md         # Module-specific documentation
    └── templates/        # Optional directory for message or other templates
        └── your_template.tpl
```

## Development Workflow

Follow these steps to create a new module:

1.  **Identify the Resource Type:** Determine which Datadog resource type you want to support (e.g., `datadog_synthetics_test`, `datadog_service_level_objective`). Refer to the [Datadog Terraform Provider documentation](https://registry.terraform.io/providers/DataDog/datadog/latest/docs).

2.  **Create the Module Directory and Files:**
    ```bash
    mkdir -p modules/your_module_name
    touch modules/your_module_name/{main.tf,variables.tf,outputs.tf,README.md}
    # If needed, create a templates directory
    # mkdir modules/your_module_name/templates
    ```

3.  **Implement the Module Logic (`main.tf`):**
    -   Define the `datadog_RESOURCE_TYPE` resource.
    -   Use variables (`var.variable_name`) for all configurable parameters.
    -   Implement `for_each` if the module is designed to create multiple resources from a map input (similar to `modules/multiple_monitors`).
    -   Include proper resource naming following the `[env]-[team]-[service]-[resource-type]` convention.
    -   Use dynamic blocks for complex nested structures (like dashboard widgets or monitor thresholds).
    -   Ensure proper tagging, potentially merging global tags with resource-specific tags.

4.  **Define Input Variables (`variables.tf`):**
    -   Define all input variables the module will accept.
    -   Include clear `description` for each variable.
    -   Specify the `type` of the variable.
    -   Set `default` values for optional parameters.
    -   Add `validation` rules to enforce expected input formats or values.

5.  **Define Output Values (`outputs.tf`):**
    -   Define the values that the module will output.
    -   Typically include the resource `id` and `name`.
    -   Include any other useful attributes or generated values.
    -   Consider including a URL to view the resource in the Datadog UI if applicable.

6.  **Write Module Documentation (`README.md`):**
    -   Provide a clear description of what the module does.
    -   Include usage examples showing how to call the module from a `.tfvars` file or another Terraform configuration.
    -   Document all input variables with their descriptions, types, defaults, and whether they are required.
    -   Document all output values.
    -   Include any resource-specific information or common configurations.

7.  **Create Example Configuration (`examples/your_module_name/`):**
    -   Create a directory for your example: `mkdir -p examples/your_module_name`.
    -   Create example files (e.g., `main.tf`, `variables.tf`, `outputs.tf`, `README.md`) that demonstrate how to use your new module. This example should be runnable independently or easily adaptable.

8.  **Update Root `main.tf`:**
    -   Add a module block in the root `main.tf` to include your new module, referencing its source path (`./modules/your_module_name`).
    -   Map the relevant variable from the environment `.tfvars` files (e.g., `var.your_resource_type`) to the module's input variable.

9.  **Update Root `variables.tf`:**
    -   Add a variable definition in the root `variables.tf` for the new resource type (e.g., `variable "your_resource_type" { type = any; description = "Map of your resource type to create"; default = {} }`).

10. **Update Documentation:**
    -   Update the main `README.md` (Project Structure, Extending the Project sections).
    -   Update the `docs/USAGE_GUIDE.md` to mention the new resource type and how to define it in environment `.tfvars` files.
    -   Update the CLI tool documentation if it should support generating templates for this new resource type.

11. **Test the Module:**
    -   Use your example configuration to test the module.
    -   Run `terraform init`, `terraform validate`, `terraform plan`, and `terraform apply` (in a safe environment) to ensure the module works as expected.

## Best Practices for Module Development

-   **Reusability:** Design modules to be as generic and reusable as possible.
-   **Input Variables:** Expose all necessary configurations as input variables. Avoid hardcoding values within the module.
-   **Output Values:** Provide useful output values that can be referenced by other modules or configurations.
-   **Versioning:** Consider versioning your modules if they are intended for use across multiple projects or teams.
-   **Documentation:** Comprehensive documentation is key for others to understand and use your module effectively.

By following these steps and best practices, you can successfully extend this project skeleton to support additional Datadog resource types.
