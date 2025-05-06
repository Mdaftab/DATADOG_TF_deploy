# Production environment configuration
environment = "prod"

global_tags = {
  managed_by = "terraform"
  team       = "platform"
  env        = "prod"
}

# Production environment dashboards
dashboards = {
  service_overview = {
    title       = "PROD - Service Overview Dashboard"
    description = "Key metrics for our service in production"
    is_read_only = true # Protect production dashboards
    
    widgets = [
      {
        definition_type = "timeseries"
        title = "Service Latency"
        request = {
          query = "avg:service.latency{env:prod} by {service}"
          display_type = "line"
        }
        markers = [
          {
            display_type = "error dashed"
            value = "200" # Strict SLA for production
            label = "SLA Threshold"
          }
        ]
      },
      {
        definition_type = "timeseries"
        title = "Error Rate"
        request = {
          query = "sum:service.errors{env:prod}.as_rate() / sum:service.requests{env:prod}.as_rate() * 100"
          display_type = "area"
        }
      },
      {
        definition_type = "toplist"
        title = "Top Endpoints by Request Count"
        request = {
          query = "top(sum:service.requests{env:prod} by {endpoint}.as_count(), 10, 'sum', 'desc')"
        }
      }
    ]
    
    tags = ["service:api", "sla:tier1"]
  }
}

# Production environment monitors - strict thresholds with alerting
monitors = {
  api_latency = {
    name    = "PROD - High API Latency"
    type    = "metric alert"
    message = <<-EOT
      Service latency is above threshold in production.
      
      ## Impact
      This is affecting user experience and may breach our SLAs.
      
      ## Investigation
      - Check for recent deployments
      - Look for increased traffic patterns
      - Verify database performance
      
      @slack-ops-alerts @pagerduty
    EOT
    query   = "avg(last_5m):avg:service.latency{env:prod,service:api} > 200"
    
    thresholds = {
      critical          = "200"
      critical_recovery = "150"
      warning           = "150"
      warning_recovery  = "100"
    }
    
    notify_no_data = true
    no_data_timeframe = 10
    renotify_interval = 15 # More frequent reminders for production
    escalation_message = "CRITICAL: Service latency is still above threshold. This is breaching our SLA! @pagerduty-high"
    
    tags = ["service:api", "sla:tier1", "priority:p1"]
  },
  
  error_rate = {
    name    = "PROD - High Error Rate"
    type    = "metric alert"
    message = "Error rate is above 0.5% for the production service. This is affecting users. @slack-ops-alerts @pagerduty"
    query   = "sum(last_5m):sum:service.errors{env:prod}.as_rate() / sum:service.requests{env:prod}.as_rate() * 100 > 0.5"
    
    thresholds = {
      critical          = "0.5" # Stricter threshold for production
      critical_recovery = "0.2"
    }
    
    tags = ["monitor:error-rate", "priority:p1"]
  }
}