module "service_dashboard" {
  source = "../../modules/dashboard"

  title       = "Service Overview Dashboard"
  description = "Key metrics for our service"
  layout_type = "ordered"
  
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
          value = "200"
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
      markers = [
        {
          display_type = "error dashed"
          value = "1"
          label = "Error threshold"
        }
      ]
    },
    {
      definition_type = "toplist"
      title = "Top Endpoints by Request Count"
      request = {
        query = "top(sum:service.requests{env:prod} by {endpoint}.as_count(), 10, 'sum', 'desc')"
      }
    }
  ]
  
  tags = ["team:backend", "env:prod", "service:api"]
}