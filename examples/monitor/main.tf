module "high_latency_monitor" {
  source = "../../modules/monitor"

  name    = "High API Latency"
  type    = "metric alert"
  message = <<-EOT
    Service latency is above threshold.
    
    ## Impact
    This could indicate performance issues affecting user experience.
    
    ## Investigation
    - Check for recent deployments
    - Look for increased traffic patterns
    - Verify database performance
    
    @slack-ops-alerts
  EOT
  
  query   = "avg(last_5m):avg:service.latency{env:${var.environment},service:${var.service_name}} > ${var.latency_threshold}"
  
  thresholds = {
    critical          = var.latency_threshold
    critical_recovery = var.latency_recovery_threshold
    warning           = var.latency_warning_threshold
    warning_recovery  = var.latency_warning_recovery_threshold
  }
  
  notify_no_data = true
  no_data_timeframe = 10
  require_full_window = false
  
  renotify_interval = 30
  escalation_message = "Service latency is still above threshold after 30 minutes. Please escalate! @pagerduty"
  
  tags = [
    "team:${var.team}",
    "env:${var.environment}",
    "service:${var.service_name}",
    "managed-by:terraform"
  ]
}