# Datadog Monitor Module

This module creates a customizable Datadog monitor.

## Usage

```hcl
module "monitor" {
  source = "../../modules/monitor"

  name    = "High CPU Usage"
  type    = "metric alert"
  message = "CPU usage is above threshold. @slack-alerts"
  query   = "avg(last_5m):avg:system.cpu.user{app:my-app} by {host} > 80"
  
  thresholds = {
    critical          = "80"
    critical_recovery = "70"
    warning           = "75"
    warning_recovery  = "65"
  }
  
  notify_no_data = true
  no_data_timeframe = 20
  require_full_window = false
  
  renotify_interval = 60
  escalation_message = "CPU usage is still high after 1 hour. Please investigate. @slack-urgent"
  
  tags = ["team:devops", "environment:prod", "application:my-app"]
}
```

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|----------|
| name | Name of the monitor | string | n/a | yes |
| type | Type of the monitor | string | n/a | yes |
| message | Message included with notifications for this monitor | string | n/a | yes |
| query | Query defines when the monitor triggers | string | n/a | yes |
| tags | List of tags to associate with the monitor | list(string) | [] | no |
| notify_no_data | Whether to notify when no data is received | bool | false | no |
| no_data_timeframe | Number of minutes before notifying when no data is received | number | 10 | no |
| notify_audit | Whether to notify on changes to the monitor | bool | false | no |
| timeout_h | Number of hours of no data after which the monitor will resolve from an alert state | number | 0 | no |
| include_tags | Whether to include triggering tags in notification messages | bool | true | no |
| require_full_window | Whether the monitor needs a full window of data before evaluating | bool | true | no |
| renotify_interval | Number of minutes after last notification before re-notifying on alert conditions | number | 0 | no |
| escalation_message | Message to include with re-notifications | string | "" | no |
| thresholds | Alert thresholds of the monitor | map(string) | null | no |
| threshold_windows | Mapping of threshold windows used in the monitor | map(string) | null | no |

## Outputs

| Name | Description |
|------|-------------|
| monitor_id | ID of the created monitor |
| monitor_name | Name of the created monitor |

## Monitor Types

The module supports all Datadog monitor types:

- `metric alert`: Threshold-based alert on a metric
- `service check`: Alert on the status of a service check
- `event alert`: Alert when events match a query
- `query alert`: Alert when a query exceeds a threshold
- `composite`: Combined alert based on multiple monitors
- `log alert`: Alert when logs match a query
- `process alert`: Alert on process status
- `rum alert`: Real User Monitoring alert
- `synthetics alert`: Alert on synthetic test results
- `trace-analytics alert`: APM trace analytics alert
- `slo alert`: Alert on SLO status

## Notification Syntax

Use @-notifications in the message parameter:

- `@slack-channel`: Notify a Slack channel
- `@teams-team`: Notify a Microsoft Teams team
- `@pagerduty`: Create a PagerDuty incident
- `@email@example.com`: Email a specific address
- `@all`: Notify all people subscribed to the monitor
- `@team:name`: Notify all members of a specific team

## Threshold Format

Thresholds should be provided as a map with these possible keys:
- `critical`: Threshold at which to trigger a critical alert
- `critical_recovery`: Threshold at which to recover from a critical alert
- `warning`: Threshold at which to trigger a warning alert
- `warning_recovery`: Threshold at which to recover from a warning alert
- `ok`: Threshold for the OK state