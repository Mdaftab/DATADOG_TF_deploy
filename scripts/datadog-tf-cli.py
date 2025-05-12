#!/usr/bin/env python3
import click
import yaml
import os
import subprocess
import json
import sys
from typing import Dict, Any, List, Optional
import re
from datetime import datetime

# ANSI color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_success(message: str):
    """Print success message in green"""
    click.echo(f"{Colors.GREEN}{message}{Colors.ENDC}")

def print_warning(message: str):
    """Print warning message in yellow"""
    click.echo(f"{Colors.YELLOW}{message}{Colors.ENDC}")

def print_error(message: str):
    """Print error message in red"""
    click.echo(f"{Colors.RED}{message}{Colors.ENDC}", err=True)

def print_info(message: str):
    """Print info message in blue"""
    click.echo(f"{Colors.BLUE}{message}{Colors.ENDC}")

def print_header(message: str):
    """Print header message in bold purple"""
    click.echo(f"\n{Colors.HEADER}{Colors.BOLD}{message}{Colors.ENDC}\n")

def validate_yaml(config_path: str) -> Dict[Any, Any]:
    """Validate YAML configuration file"""
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
            
        # Basic schema validation
        if not isinstance(config, dict):
            raise ValueError("Configuration must be a dictionary")
            
        # Validate based on resource type
        if 'monitors' in config:
            for name, monitor in config['monitors'].items():
                required_fields = ['name', 'type', 'query']
                for field in required_fields:
                    if field not in monitor:
                        raise ValueError(f"Monitor '{name}' missing required field: {field}")
                
                # Validate monitor type
                valid_types = ["composite", "event alert", "log alert", "metric alert", 
                              "process alert", "query alert", "rum alert", "service check", 
                              "synthetics alert", "trace-analytics alert", "slo alert"]
                if 'type' in monitor and monitor['type'] not in valid_types:
                    raise ValueError(f"Monitor '{name}' has invalid type: {monitor['type']}. Valid types are: {', '.join(valid_types)}")
                
                # Validate tags
                if 'tags' in monitor:
                    required_tag_prefixes = ['service:', 'env:']
                    for prefix in required_tag_prefixes:
                        if not any(tag.startswith(prefix) for tag in monitor['tags']):
                            print_warning(f"Monitor '{name}' is missing recommended tag prefix: {prefix}")
                
        elif 'dashboards' in config:
            for name, dashboard in config['dashboards'].items():
                required_fields = ['title', 'widgets']
                for field in required_fields:
                    if field not in dashboard:
                        raise ValueError(f"Dashboard '{name}' missing required field: {field}")
                
                # Validate widgets
                if 'widgets' in dashboard:
                    for i, widget in enumerate(dashboard['widgets']):
                        if 'type' not in widget:
                            raise ValueError(f"Dashboard '{name}' widget #{i+1} missing 'type' field")
                        if 'title' not in widget:
                            raise ValueError(f"Dashboard '{name}' widget #{i+1} missing 'title' field")
                
        elif 'slos' in config:
            for name, slo in config['slos'].items():
                required_fields = ['name', 'type', 'target', 'timeframe']
                for field in required_fields:
                    if field not in slo:
                        raise ValueError(f"SLO '{name}' missing required field: {field}")
                
                # Validate SLO type
                valid_types = ["metric", "monitor"]
                if 'type' in slo and slo['type'] not in valid_types:
                    raise ValueError(f"SLO '{name}' has invalid type: {slo['type']}. Valid types are: {', '.join(valid_types)}")
                
                # Validate target
                if 'target' in slo:
                    try:
                        target = float(slo['target'])
                        if target < 0 or target > 100:
                            raise ValueError(f"SLO '{name}' target must be between 0 and 100")
                    except (ValueError, TypeError):
                        raise ValueError(f"SLO '{name}' target must be a number between 0 and 100")
                
                # Validate timeframe
                valid_timeframes = ["7d", "30d", "90d"]
                if 'timeframe' in slo and slo['timeframe'] not in valid_timeframes:
                    raise ValueError(f"SLO '{name}' has invalid timeframe: {slo['timeframe']}. Valid timeframes are: {', '.join(valid_timeframes)}")
        
        elif 'synthetics' in config:
            for name, test in config['synthetics'].items():
                required_fields = ['name', 'type', 'request']
                for field in required_fields:
                    if field not in test:
                        raise ValueError(f"Synthetic test '{name}' missing required field: {field}")
                
                # Validate test type
                valid_types = ["api", "browser"]
                if 'type' in test and test['type'] not in valid_types:
                    raise ValueError(f"Synthetic test '{name}' has invalid type: {test['type']}. Valid types are: {', '.join(valid_types)}")
        
        # Check for recommended fields
        if 'monitors' in config:
            for name, monitor in config['monitors'].items():
                if 'message' not in monitor:
                    print_warning(f"Monitor '{name}' is missing recommended field: message")
                if 'tags' not in monitor:
                    print_warning(f"Monitor '{name}' is missing recommended field: tags")
        
        return config
    except yaml.YAMLError as e:
        print_error(f"Error parsing YAML: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print_error(f"Configuration file not found: {config_path}")
        sys.exit(1)
    except ValueError as e:
        print_error(f"Configuration validation error: {e}")
        sys.exit(1)

def get_project_root() -> str:
    """Get the project root directory"""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def ensure_directory(path: str):
    """Ensure directory exists, create if it doesn't"""
    os.makedirs(os.path.dirname(path), exist_ok=True)

def generate_template(resource_type: str, output_path: str, template_name: Optional[str] = None):
    """Generate template YAML for specified resource type"""
    # Basic templates
    basic_templates = {
        'monitor': {
            'monitors': {
                'example_monitor': {
                    'name': 'Example Monitor',
                    'type': 'metric alert',
                    'query': 'avg(last_5m):avg:system.cpu.user{*} > 80',
                    'message': 'CPU usage is high\n\n@slack-channel @pagerduty-service',
                    'tags': ['service:example', 'env:prod', 'team:devops'],
                    'threshold': 80,
                    'notification_channels': ['@slack-channel', '@pagerduty-service']
                }
            }
        },
        'dashboard': {
            'dashboards': {
                'example_dashboard': {
                    'title': 'Example Dashboard',
                    'description': 'Example dashboard with common widgets',
                    'widgets': [
                        {
                            'type': 'timeseries',
                            'title': 'CPU Usage',
                            'query': 'avg:system.cpu.user{*}'
                        },
                        {
                            'type': 'timeseries',
                            'title': 'Memory Usage',
                            'query': 'avg:system.mem.used{*}'
                        }
                    ]
                }
            }
        },
        'slo': {
            'slos': {
                'example_slo': {
                    'name': 'Example Service Level Objective',
                    'type': 'metric',
                    'target': 99.9,
                    'timeframe': '30d',
                    'query': {
                        'numerator': 'sum:requests.successful{service:example}.as_count()',
                        'denominator': 'sum:requests.total{service:example}.as_count()'
                    },
                    'tags': ['service:example', 'env:prod', 'team:devops']
                }
            }
        },
        'synthetic': {
            'synthetics': {
                'example_api_test': {
                    'name': 'Example API Test',
                    'type': 'api',
                    'request': {
                        'method': 'GET',
                        'url': 'https://example.com/api/health',
                        'timeout': 30
                    },
                    'assertions': [
                        {
                            'type': 'statusCode',
                            'operator': 'is',
                            'target': 200
                        },
                        {
                            'type': 'responseTime',
                            'operator': 'lessThan',
                            'target': 1000
                        }
                    ],
                    'locations': ['aws:us-east-1', 'aws:eu-west-1'],
                    'tags': ['service:example', 'env:prod', 'team:devops']
                }
            }
        }
    }
    
    # Specialized templates
    specialized_templates = {
        'api-monitoring': {
            'monitors': {
                'api_latency': {
                    'name': 'API Latency Monitor',
                    'type': 'metric alert',
                    'query': 'avg(last_5m):avg:trace.http.request.duration{service:YOUR_SERVICE} > 1000',
                    'message': 'API latency is above threshold of 1000ms\n\n@slack-your-channel @pagerduty-service',
                    'threshold': 1000,
                    'tags': ['service:YOUR_SERVICE', 'env:prod', 'team:backend'],
                    'notification_channels': ['@slack-your-channel', '@pagerduty-service']
                },
                'error_rate': {
                    'name': 'API Error Rate Monitor',
                    'type': 'metric alert',
                    'query': 'sum(last_5m):sum:trace.http.request.errors{service:YOUR_SERVICE}.as_count() / sum:trace.http.request.hits{service:YOUR_SERVICE}.as_count() * 100 > 5',
                    'message': 'Error rate is above 5%\n\n@slack-your-channel @pagerduty-service',
                    'threshold': 5,
                    'tags': ['service:YOUR_SERVICE', 'env:prod', 'team:backend']
                }
            },
            'dashboards': {
                'api_overview': {
                    'title': 'API Overview Dashboard',
                    'description': 'Overview of API performance metrics',
                    'widgets': [
                        {
                            'type': 'timeseries',
                            'title': 'API Latency',
                            'query': 'avg:trace.http.request.duration{service:YOUR_SERVICE}'
                        },
                        {
                            'type': 'timeseries',
                            'title': 'Error Rate',
                            'query': 'sum:trace.http.request.errors{service:YOUR_SERVICE}.as_count() / sum:trace.http.request.hits{service:YOUR_SERVICE}.as_count() * 100'
                        },
                        {
                            'type': 'toplist',
                            'title': 'Slowest Endpoints',
                            'query': 'avg:trace.http.request.duration{service:YOUR_SERVICE} by {resource_name}'
                        }
                    ]
                }
            }
        },
        'database-monitoring': {
            'monitors': {
                'db_connections': {
                    'name': 'Database Connection Pool Monitor',
                    'type': 'metric alert',
                    'query': 'avg(last_5m):avg:database.connections.usage{service:YOUR_DB} > 80',
                    'message': 'Database connection pool usage is high (>80%)\n\n@slack-your-channel @pagerduty-service',
                    'threshold': 80,
                    'tags': ['service:YOUR_DB', 'env:prod', 'team:dba'],
                    'notification_channels': ['@slack-your-channel', '@pagerduty-service']
                },
                'db_latency': {
                    'name': 'Database Query Latency Monitor',
                    'type': 'metric alert',
                    'query': 'avg(last_5m):avg:database.query.duration{service:YOUR_DB} > 500',
                    'message': 'Database query latency is high (>500ms)\n\n@slack-your-channel @pagerduty-service',
                    'threshold': 500,
                    'tags': ['service:YOUR_DB', 'env:prod', 'team:dba']
                },
                'db_disk_usage': {
                    'name': 'Database Disk Usage Monitor',
                    'type': 'metric alert',
                    'query': 'avg(last_5m):avg:database.disk.usage{service:YOUR_DB} > 85',
                    'message': 'Database disk usage is high (>85%)\n\n@slack-your-channel @pagerduty-service',
                    'threshold': 85,
                    'tags': ['service:YOUR_DB', 'env:prod', 'team:dba']
                }
            },
            'dashboards': {
                'db_overview': {
                    'title': 'Database Overview Dashboard',
                    'description': 'Overview of database performance metrics',
                    'widgets': [
                        {
                            'type': 'timeseries',
                            'title': 'Connection Pool Usage',
                            'query': 'avg:database.connections.usage{service:YOUR_DB}'
                        },
                        {
                            'type': 'timeseries',
                            'title': 'Query Latency',
                            'query': 'avg:database.query.duration{service:YOUR_DB}'
                        },
                        {
                            'type': 'timeseries',
                            'title': 'Disk Usage',
                            'query': 'avg:database.disk.usage{service:YOUR_DB}'
                        },
                        {
                            'type': 'toplist',
                            'title': 'Slowest Queries',
                            'query': 'avg:database.query.duration{service:YOUR_DB} by {query_hash}'
                        }
                    ]
                }
            }
        },
        'microservice-monitoring': {
            'monitors': {
                'service_latency': {
                    'name': 'Microservice Latency Monitor',
                    'type': 'metric alert',
                    'query': 'avg(last_5m):avg:trace.http.request.duration{service:YOUR_SERVICE} > 500',
                    'message': 'Microservice latency is above threshold of 500ms\n\n@slack-your-channel @pagerduty-service',
                    'threshold': 500,
                    'tags': ['service:YOUR_SERVICE', 'env:prod', 'team:backend'],
                    'notification_channels': ['@slack-your-channel', '@pagerduty-service']
                },
                'error_rate': {
                    'name': 'Microservice Error Rate Monitor',
                    'type': 'metric alert',
                    'query': 'sum(last_5m):sum:trace.http.request.errors{service:YOUR_SERVICE}.as_count() / sum:trace.http.request.hits{service:YOUR_SERVICE}.as_count() * 100 > 2',
                    'message': 'Error rate is above 2%\n\n@slack-your-channel @pagerduty-service',
                    'threshold': 2,
                    'tags': ['service:YOUR_SERVICE', 'env:prod', 'team:backend']
                },
                'memory_usage': {
                    'name': 'Microservice Memory Usage Monitor',
                    'type': 'metric alert',
                    'query': 'avg(last_5m):avg:docker.mem.rss{service:YOUR_SERVICE} / avg:docker.mem.limit{service:YOUR_SERVICE} * 100 > 85',
                    'message': 'Memory usage is above 85%\n\n@slack-your-channel @pagerduty-service',
                    'threshold': 85,
                    'tags': ['service:YOUR_SERVICE', 'env:prod', 'team:backend']
                },
                'cpu_usage': {
                    'name': 'Microservice CPU Usage Monitor',
                    'type': 'metric alert',
                    'query': 'avg(last_5m):avg:docker.cpu.usage{service:YOUR_SERVICE} > 80',
                    'message': 'CPU usage is above 80%\n\n@slack-your-channel @pagerduty-service',
                    'threshold': 80,
                    'tags': ['service:YOUR_SERVICE', 'env:prod', 'team:backend']
                }
            },
            'dashboards': {
                'service_overview': {
                    'title': 'Microservice Overview Dashboard',
                    'description': 'Overview of microservice performance metrics',
                    'widgets': [
                        {
                            'type': 'timeseries',
                            'title': 'Request Latency',
                            'query': 'avg:trace.http.request.duration{service:YOUR_SERVICE}'
                        },
                        {
                            'type': 'timeseries',
                            'title': 'Error Rate',
                            'query': 'sum:trace.http.request.errors{service:YOUR_SERVICE}.as_count() / sum:trace.http.request.hits{service:YOUR_SERVICE}.as_count() * 100'
                        },
                        {
                            'type': 'timeseries',
                            'title': 'Memory Usage',
                            'query': 'avg:docker.mem.rss{service:YOUR_SERVICE} / avg:docker.mem.limit{service:YOUR_SERVICE} * 100'
                        },
                        {
                            'type': 'timeseries',
                            'title': 'CPU Usage',
                            'query': 'avg:docker.cpu.usage{service:YOUR_SERVICE}'
                        },
                        {
                            'type': 'toplist',
                            'title': 'Slowest Endpoints',
                            'query': 'avg:trace.http.request.duration{service:YOUR_SERVICE} by {resource_name}'
                        }
                    ]
                }
            },
            'slos': {
                'service_availability': {
                    'name': 'Microservice Availability',
                    'type': 'metric',
                    'target': 99.9,
                    'timeframe': '30d',
                    'query': {
                        'numerator': 'sum:trace.http.request.hits{service:YOUR_SERVICE,http.status_code:2xx}.as_count()',
                        'denominator': 'sum:trace.http.request.hits{service:YOUR_SERVICE}.as_count()'
                    },
                    'tags': ['service:YOUR_SERVICE', 'env:prod', 'team:backend']
                },
                'service_latency': {
                    'name': 'Microservice Latency SLO',
                    'type': 'metric',
                    'target': 99.0,
                    'timeframe': '30d',
                    'query': {
                        'numerator': 'sum:trace.http.request.hits{service:YOUR_SERVICE,http.request.duration:<200}.as_count()',
                        'denominator': 'sum:trace.http.request.hits{service:YOUR_SERVICE}.as_count()'
                    },
                    'tags': ['service:YOUR_SERVICE', 'env:prod', 'team:backend']
                }
            }
        }
    }
    
    # Determine which template to use
    template_data = None
    
    # Check if it's a basic resource type
    if resource_type in basic_templates:
        template_data = basic_templates[resource_type]
    # Check if it's a specialized template
    elif template_name and template_name in specialized_templates:
        template_data = specialized_templates[template_name]
    # If template_name is provided but not found in specialized templates
    elif template_name:
        print_error(f"Unknown template: {template_name}")
        print_info(f"Available templates: {', '.join(specialized_templates.keys())}")
        sys.exit(1)
    # If resource_type is not found in basic templates
    else:
        print_error(f"Unknown resource type: {resource_type}")
        print_info(f"Available resource types: {', '.join(basic_templates.keys())}")
        print_info(f"Available specialized templates: {', '.join(specialized_templates.keys())}")
        sys.exit(1)
    
    # Ensure path is relative to examples/templates if not absolute
    if not os.path.isabs(output_path):
        output_path = os.path.join(get_project_root(), 'examples', 'templates', output_path)
    
    # Ensure directory exists
    ensure_directory(output_path)
    
    with open(output_path, 'w') as f:
        yaml.dump(template_data, f, default_flow_style=False)
    
    print_success(f"Template generated at: {output_path}")
    
    # Print a helpful message about what to do next
    print_info("\nNext steps:")
    print_info("1. Customize the template for your specific needs")
    print_info("2. Validate your configuration:")
    print_info(f"   python scripts/datadog-tf-cli.py validate {output_path}")
    print_info("3. Preview the changes:")
    print_info(f"   python scripts/datadog-tf-cli.py plan {output_path}")
    print_info("4. Apply the changes:")
    print_info(f"   python scripts/datadog-tf-cli.py apply {output_path}")

def terraform_plan(config_path: str):
    """Run terraform plan with the specified config"""
    # First validate the config
    validate_yaml(config_path)
    
    print_header("Running Terraform Plan")
    
    # Run terraform plan
    result = subprocess.run(['terraform', 'plan'], capture_output=True, text=True)
    click.echo(result.stdout)
    if result.returncode != 0:
        print_error("Terraform plan failed!")
        sys.exit(1)
    else:
        print_success("Terraform plan completed successfully")

def terraform_apply(config_path: str, auto_approve: bool = False):
    """Apply the configuration"""
    # First do a plan
    terraform_plan(config_path)
    
    if auto_approve or click.confirm('Do you want to apply these changes?'):
        print_header("Applying Terraform Changes")
        
        cmd = ['terraform', 'apply']
        if auto_approve:
            cmd.append('-auto-approve')
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        click.echo(result.stdout)
        if result.returncode != 0:
            print_error("Terraform apply failed!")
            sys.exit(1)
        else:
            print_success("Terraform apply completed successfully")

def list_templates():
    """List available templates"""
    print_header("Available Templates")
    
    templates = {
        "Basic Templates": [
            {"name": "monitor", "description": "Basic monitor template"},
            {"name": "dashboard", "description": "Basic dashboard template"},
            {"name": "slo", "description": "Basic SLO template"},
            {"name": "synthetic", "description": "Basic synthetic test template"}
        ],
        "Specialized Templates": [
            {"name": "api-monitoring", "description": "Complete API monitoring solution with monitors and dashboard"},
            {"name": "database-monitoring", "description": "Database monitoring solution with connection, latency, and disk usage monitors"},
            {"name": "microservice-monitoring", "description": "Comprehensive microservice monitoring with SLOs, monitors, and dashboard"}
        ]
    }
    
    for category, items in templates.items():
        print_info(f"\n{category}:")
        for item in items:
            click.echo(f"  {Colors.BOLD}{item['name']}{Colors.ENDC}: {item['description']}")

def interactive_template():
    """Interactive template creation"""
    print_header("Interactive Template Creation")
    
    # Step 1: Choose template type
    print_info("Step 1: Choose a template type")
    template_types = [
        ("Basic monitor", "monitor"),
        ("Basic dashboard", "dashboard"),
        ("Basic SLO", "slo"),
        ("Basic synthetic test", "synthetic"),
        ("API monitoring solution", "api-monitoring"),
        ("Database monitoring solution", "database-monitoring"),
        ("Microservice monitoring solution", "microservice-monitoring")
    ]
    
    for i, (name, _) in enumerate(template_types):
        click.echo(f"  {i+1}. {name}")
    
    choice = click.prompt("Enter your choice (1-7)", type=int, default=1)
    if choice < 1 or choice > len(template_types):
        print_error("Invalid choice")
        sys.exit(1)
    
    template_name = template_types[choice-1][1]
    
    # Step 2: Enter output path
    print_info("\nStep 2: Enter output path")
    output_path = click.prompt("Enter output path", default=f"{template_name}-{datetime.now().strftime('%Y%m%d%H%M%S')}.yaml")
    
    # Step 3: Generate template
    print_info("\nStep 3: Generating template")
    
    # Determine if it's a basic or specialized template
    if template_name in ["monitor", "dashboard", "slo", "synthetic"]:
        generate_template(template_name, output_path)
    else:
        # For specialized templates, we pass the template name as the second parameter
        generate_template("specialized", output_path, template_name)
    
    print_success(f"\nTemplate generated at: {output_path}")

def bulk_operation(operation: str, config_dir: str):
    """Perform bulk operations on multiple configuration files"""
    if not os.path.isdir(config_dir):
        print_error(f"Directory not found: {config_dir}")
        sys.exit(1)
    
    yaml_files = [f for f in os.listdir(config_dir) if f.endswith('.yaml') or f.endswith('.yml')]
    
    if not yaml_files:
        print_error(f"No YAML files found in directory: {config_dir}")
        sys.exit(1)
    
    print_header(f"Performing bulk {operation} on {len(yaml_files)} files")
    
    for yaml_file in yaml_files:
        config_path = os.path.join(config_dir, yaml_file)
        print_info(f"\nProcessing: {config_path}")
        
        if operation == 'validate':
            try:
                validate_yaml(config_path)
                print_success(f"✓ {yaml_file} is valid")
            except Exception as e:
                print_error(f"✗ {yaml_file} is invalid: {str(e)}")
        elif operation == 'plan':
            try:
                terraform_plan(config_path)
            except Exception as e:
                print_error(f"✗ Failed to plan {yaml_file}: {str(e)}")
        elif operation == 'apply':
            try:
                terraform_apply(config_path, auto_approve=True)
            except Exception as e:
                print_error(f"✗ Failed to apply {yaml_file}: {str(e)}")
    
    print_success(f"\nBulk {operation} completed")

@click.group()
def cli():
    """Datadog Terraform CLI - Simplify Datadog resource deployment"""
    pass

@cli.command()
@click.argument('resource_type')
@click.argument('output_path')
@click.option('--template', '-t', help='Specialized template to use')
def template(resource_type: str, output_path: str, template: Optional[str] = None):
    """Generate a template YAML configuration"""
    generate_template(resource_type, output_path, template)

@cli.command()
def interactive():
    """Interactive template creation wizard"""
    interactive_template()

@cli.command()
def list():
    """List available templates"""
    list_templates()

@cli.command()
@click.argument('config_path')
def validate(config_path: str):
    """Validate a YAML configuration file"""
    config = validate_yaml(config_path)
    print_success("Configuration is valid!")

@cli.command()
@click.argument('config_path')
def plan(config_path: str):
    """Preview changes to be applied"""
    terraform_plan(config_path)

@cli.command()
@click.argument('config_path')
@click.option('--auto-approve', '-y', is_flag=True, help='Automatically approve and apply changes')
def apply(config_path: str, auto_approve: bool):
    """Apply the configuration"""
    terraform_apply(config_path, auto_approve)

@cli.command()
@click.argument('operation', type=click.Choice(['validate', 'plan', 'apply']))
@click.argument('config_dir')
def bulk(operation: str, config_dir: str):
    """Perform bulk operations on multiple configuration files"""
    bulk_operation(operation, config_dir)

@cli.command()
def version():
    """Show version information"""
    print_info("Datadog Terraform CLI v1.0.0")
    print_info("A developer-friendly tool for deploying Datadog resources using Terraform")

if __name__ == '__main__':
    cli()
