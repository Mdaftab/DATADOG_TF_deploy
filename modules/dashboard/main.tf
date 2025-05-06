# Dashboard module - main configuration

resource "datadog_dashboard" "dashboard" {
  title       = var.title
  description = var.description
  layout_type = var.layout_type
  is_read_only = var.is_read_only
  
  dynamic "widget" {
    for_each = var.widgets
    content {
      layout = lookup(widget.value, "layout", null)
      
      dynamic "time_series_definition" {
        for_each = lookup(widget.value, "definition_type", "") == "timeseries" ? [1] : []
        content {
          title = lookup(widget.value, "title", null)
          request {
            q = widget.value.request.query
            display_type = lookup(widget.value.request, "display_type", "line")
          }
          
          dynamic "marker" {
            for_each = lookup(widget.value, "markers", [])
            content {
              display_type = lookup(marker.value, "display_type", "error dashed")
              value = marker.value.value
              label = lookup(marker.value, "label", null)
            }
          }
        }
      }
      
      dynamic "toplist_definition" {
        for_each = lookup(widget.value, "definition_type", "") == "toplist" ? [1] : []
        content {
          title = lookup(widget.value, "title", null)
          request {
            q = widget.value.request.query
          }
        }
      }
      
      dynamic "group_definition" {
        for_each = lookup(widget.value, "definition_type", "") == "group" ? [1] : []
        content {
          title = lookup(widget.value, "title", null)
          layout_type = lookup(widget.value, "layout_type", "ordered")
          
          dynamic "widget" {
            for_each = lookup(widget.value, "widgets", [])
            content {
              # Nested widgets configuration would go here
              # This is a simplified version
            }
          }
        }
      }

      # Additional widget types can be added as needed
    }
  }

  tags = var.tags
}