output "dashboard_id" {
  description = "ID of the created dashboard"
  value       = datadog_dashboard.dashboard.id
}

output "dashboard_url" {
  description = "URL of the created dashboard"
  value       = datadog_dashboard.dashboard.url
}