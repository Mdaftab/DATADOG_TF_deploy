# Dev environment configuration
environment = "dev"

global_tags = {
  managed_by = "terraform"
  team       = "platform"
  env        = "dev"
}

# Development environment dashboards
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
            value = "500" # Higher threshold for dev
            label = "SLA Threshold"
          }
        ]
      },
      {
        definition_type = "timeseries"
        title = "Error Rate"
        request = {
          query = "sum:service.errors{env:dev}.as_rate() / sum:service.requests{env:dev}.as_rate() * 100"
          display_type = "area"
        }
      }
    ]
    
    tags = ["service:api"]
  }
}

# Development environment monitors
monitors = {
  # Less strict thresholds for dev environment
  api_latency = {
    name    = "DEV - High API Latency"
    type    = "metric alert"
    message = "Service latency is above threshold in dev. @slack-dev-alerts"
    query   = "avg(last_5m):avg:service.latency{env:dev,service:api} > 500"
    
    thresholds = {
      critical          = "500"
      critical_recovery = "400"
    }
    
    # Don't wake people up for dev issues
    notify_no_data = false
    
    tags = ["service:api"]
  }
}