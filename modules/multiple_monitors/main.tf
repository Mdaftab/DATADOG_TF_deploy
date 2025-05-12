resource "datadog_monitor" "this" {
  for_each = var.monitors

  name    = each.value.name
  type    = "metric alert"
  query   = coalesce(each.value.query, "avg(last_5m):avg:system.cpu.user{*} > ${each.value.threshold}")
  message = templatefile("${path.module}/templates/message.tpl", {
    name      = each.value.name
    threshold = each.value.threshold
    tags      = join(", ", each.value.tags)
  })

  monitor_thresholds {
    critical = each.value.threshold
    warning  = each.value.threshold * 0.8
  }

  notify_no_data     = lookup(each.value, "notify_no_data", true)
  no_data_timeframe  = lookup(each.value, "no_data_timeframe", 10)
  include_tags       = lookup(each.value, "include_tags", true)
  require_full_window = lookup(each.value, "require_full_window", true)
  renotify_interval  = lookup(each.value, "renotify_interval", 0)

  tags = each.value.tags
} 