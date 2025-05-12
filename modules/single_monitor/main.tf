# Monitor module - main configuration

resource "datadog_monitor" "monitor" {
  name               = var.name
  type               = var.type
  message            = var.message
  query              = var.query
  
  # Alert options
  notify_no_data     = var.notify_no_data
  no_data_timeframe  = var.notify_no_data ? var.no_data_timeframe : null
  notify_audit       = var.notify_audit
  timeout_h          = var.timeout_h
  include_tags       = var.include_tags
  require_full_window = var.require_full_window
  renotify_interval  = var.renotify_interval
  escalation_message = var.escalation_message
  
  # Thresholds
  dynamic "thresholds" {
    for_each = var.thresholds != null ? [1] : []
    content {
      ok                = lookup(var.thresholds, "ok", null)
      warning           = lookup(var.thresholds, "warning", null)
      warning_recovery  = lookup(var.thresholds, "warning_recovery", null)
      critical          = lookup(var.thresholds, "critical", null)
      critical_recovery = lookup(var.thresholds, "critical_recovery", null)
    }
  }
  
  # Notification targets
  dynamic "monitor_thresholds_monitor_threshold" {
    for_each = var.threshold_windows != null ? [1] : []
    content {
      recovery_window = lookup(var.threshold_windows, "recovery_window", null)
      trigger_window  = lookup(var.threshold_windows, "trigger_window", null)
    }
  }
  
  tags = var.tags
}