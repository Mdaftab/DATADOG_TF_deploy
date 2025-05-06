output "monitor_id" {
  description = "ID of the created monitor"
  value       = datadog_monitor.monitor.id
}

output "monitor_name" {
  description = "Name of the created monitor"
  value       = datadog_monitor.monitor.name
}