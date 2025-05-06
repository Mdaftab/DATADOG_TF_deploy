#!/bin/bash
# Script to create a new Datadog resource configuration

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if resource type was provided
if [ $# -lt 1 ]; then
  echo -e "${RED}Error: Resource type is required.${NC}"
  echo -e "Usage: $0 <resource_type> <resource_name>"
  echo -e "Available resource types: dashboard, monitor, log_monitor, apm_monitor, synthetic, slo"
  exit 1
fi

RESOURCE_TYPE=$1
RESOURCE_NAME=$2

# Check if resource name was provided
if [ -z "$RESOURCE_NAME" ]; then
  echo -e "${YELLOW}Warning: No resource name provided. Using 'new_resource' as default.${NC}"
  RESOURCE_NAME="new_resource"
fi

# Function to create a dashboard resource
create_dashboard() {
  cat << EOF
  $RESOURCE_NAME = {
    title       = "$RESOURCE_NAME Dashboard"
    description = "Description of the $RESOURCE_NAME dashboard"
    
    widgets = [
      {
        definition_type = "timeseries"
        title = "Metric Over Time"
        request = {
          query = "avg:system.cpu.user{service:$RESOURCE_NAME} by {host}"
          display_type = "line"
        }
      }
    ]
    
    tags = ["service:$RESOURCE_NAME"]
  }
EOF
}

# Function to create a monitor resource
create_monitor() {
  cat << EOF
  $RESOURCE_NAME = {
    name    = "$RESOURCE_NAME Monitor"
    type    = "metric alert"
    message = "Alert message for $RESOURCE_NAME. @slack-alerts"
    query   = "avg(last_5m):avg:system.cpu.user{service:$RESOURCE_NAME} > 80"
    
    thresholds = {
      critical          = "80"
      critical_recovery = "70"
    }
    
    tags = ["service:$RESOURCE_NAME"]
  }
EOF
}

# Function to create a log monitor resource
create_log_monitor() {
  cat << EOF
  $RESOURCE_NAME = {
    name    = "$RESOURCE_NAME Log Monitor"
    query   = "logs(\"service:$RESOURCE_NAME status:error\").index(\"main\").rollup(\"count\").last(\"5m\") > 5"
    message = "High number of error logs for $RESOURCE_NAME. @slack-alerts"
    
    tags = ["service:$RESOURCE_NAME"]
  }
EOF
}

# Function to create an APM monitor resource
create_apm_monitor() {
  cat << EOF
  $RESOURCE_NAME = {
    name    = "$RESOURCE_NAME APM Monitor"
    query   = "avg(last_5m):trace.{service:$RESOURCE_NAME}.errors > 10"
    message = "High error rate detected in $RESOURCE_NAME service. @slack-alerts"
    
    tags = ["service:$RESOURCE_NAME"]
  }
EOF
}

# Main logic
echo -e "${BLUE}Creating a new $RESOURCE_TYPE resource named '$RESOURCE_NAME'...${NC}"

# Start building the output
OUTPUT=""

# Create the resource configuration based on type
case $RESOURCE_TYPE in
  dashboard)
    OUTPUT=$(create_dashboard)
    VAR_NAME="dashboards"
    ;;
  monitor)
    OUTPUT=$(create_monitor)
    VAR_NAME="monitors"
    ;;
  log_monitor)
    OUTPUT=$(create_log_monitor)
    VAR_NAME="log_monitors"
    ;;
  apm_monitor)
    OUTPUT=$(create_apm_monitor)
    VAR_NAME="apm_monitors"
    ;;
  *)
    echo -e "${RED}Error: Unsupported resource type '$RESOURCE_TYPE'.${NC}"
    echo -e "Available resource types: dashboard, monitor, log_monitor, apm_monitor"
    exit 1
    ;;
esac

# Check if resources.auto.tfvars exists
TFVARS_FILE="resources.auto.tfvars"
if [ -f "$TFVARS_FILE" ]; then
  # Check if the variable is already defined
  if grep -q "$VAR_NAME = {" "$TFVARS_FILE"; then
    # Check if the resource is already defined
    if grep -q "$RESOURCE_NAME = {" "$TFVARS_FILE"; then
      echo -e "${RED}Error: Resource '$RESOURCE_NAME' already exists in $TFVARS_FILE.${NC}"
      exit 1
    fi
    
    # Add the resource to the existing variable
    sed -i "" "/$VAR_NAME = {/a\\
$OUTPUT
" "$TFVARS_FILE"
  else
    # Add the variable and resource
    echo -e "\n# $RESOURCE_TYPE resources\n$VAR_NAME = {\n$OUTPUT\n}" >> "$TFVARS_FILE"
  fi
else
  # Create a new file
  echo -e "# $RESOURCE_TYPE resources\n$VAR_NAME = {\n$OUTPUT\n}" > "$TFVARS_FILE"
fi

echo -e "${GREEN}Resource created successfully in $TFVARS_FILE!${NC}"
echo -e "${YELLOW}Don't forget to review and customize the generated configuration before applying.${NC}"

exit 0