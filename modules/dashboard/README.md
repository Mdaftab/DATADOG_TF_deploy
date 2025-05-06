# Datadog Dashboard Module

This module creates a customizable Datadog dashboard.

## Usage

```hcl
module "dashboard" {
  source = "../../modules/dashboard"

  title       = "My Application Dashboard"
  description = "Overview of application performance metrics"
  layout_type = "ordered"
  
  widgets = [
    {
      definition_type = "timeseries"
      title = "CPU Usage"
      request = {
        query = "avg:system.cpu.user{app:my-app} by {host}"
        display_type = "line"
      }
      markers = [
        {
          display_type = "error dashed"
          value = "80"
          label = "CPU threshold"
        }
      ]
    },
    {
      definition_type = "toplist"
      title = "Top Hosts by Memory Usage"
      request = {
        query = "top(avg:system.mem.used{app:my-app} by {host}, 10, 'mean', 'desc')"
      }
    }
  ]
  
  tags = ["team:devops", "environment:prod", "application:my-app"]
}
```

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|----------|
| title | Title of the dashboard | string | n/a | yes |
| description | Description of the dashboard | string | "" | no |
| layout_type | Layout type of the dashboard | string | "ordered" | no |
| is_read_only | Whether the dashboard is read-only | bool | false | no |
| widgets | List of widget configurations for the dashboard | any | [] | no |
| tags | List of tags to associate with the dashboard | list(string) | [] | no |

## Outputs

| Name | Description |
|------|-------------|
| dashboard_id | ID of the created dashboard |
| dashboard_url | URL of the created dashboard |

## Widget Configuration

The `widgets` variable accepts a list of maps, each representing a widget configuration.

### Time Series Widget

```hcl
{
  definition_type = "timeseries"
  title = "Widget Title"
  request = {
    query = "avg:system.cpu.user{app:my-app} by {host}"
    display_type = "line"  # Optional: line, area, or bar
  }
  markers = [  # Optional
    {
      display_type = "error dashed"
      value = "80"
      label = "Threshold Label"
    }
  ]
}
```

### Toplist Widget

```hcl
{
  definition_type = "toplist"
  title = "Top Hosts by Memory Usage"
  request = {
    query = "top(avg:system.mem.used{app:my-app} by {host}, 10, 'mean', 'desc')"
  }
}
```

Additional widget types can be added as needed for specific use cases.