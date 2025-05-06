output "monitor_id" {
  description = "ID of the created monitor"
  value       = module.high_latency_monitor.monitor_id
}

output "monitor_name" {
  description = "Name of the created monitor"
  value       = module.high_latency_monitor.monitor_name
}