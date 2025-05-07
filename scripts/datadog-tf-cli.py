#!/usr/bin/env python3
import click
import yaml
import os
import subprocess
import json
from typing import Dict, Any
import sys

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
                        
        elif 'dashboards' in config:
            for name, dashboard in config['dashboards'].items():
                required_fields = ['title', 'widgets']
                for field in required_fields:
                    if field not in dashboard:
                        raise ValueError(f"Dashboard '{name}' missing required field: {field}")
                        
        return config
    except yaml.YAMLError as e:
        click.echo(f"Error parsing YAML: {e}", err=True)
        sys.exit(1)
    except FileNotFoundError:
        click.echo(f"Configuration file not found: {config_path}", err=True)
        sys.exit(1)
    except ValueError as e:
        click.echo(f"Configuration validation error: {e}", err=True)
        sys.exit(1)

def get_project_root() -> str:
    """Get the project root directory"""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def ensure_directory(path: str):
    """Ensure directory exists, create if it doesn't"""
    os.makedirs(os.path.dirname(path), exist_ok=True)

def generate_template(resource_type: str, output_path: str):
    """Generate template YAML for specified resource type"""
    templates = {
        'monitor': {
            'name': 'Example Monitor',
            'type': 'metric alert',
            'query': 'avg(last_5m):avg:system.cpu.user{*} > 80',
            'message': 'CPU usage is high',
            'tags': ['service:example', 'env:prod'],
            'threshold': 80,
            'notification_channels': ['@slack-channel']
        },
        'dashboard': {
            'title': 'Example Dashboard',
            'description': 'Example dashboard with common widgets',
            'widgets': [
                {
                    'type': 'timeseries',
                    'title': 'CPU Usage',
                    'query': 'avg:system.cpu.user{*}'
                }
            ]
        }
    }
    
    if resource_type not in templates:
        click.echo(f"Unknown resource type: {resource_type}", err=True)
        sys.exit(1)
    
    # Ensure path is relative to examples/templates if not absolute
    if not os.path.isabs(output_path):
        output_path = os.path.join(get_project_root(), 'examples', 'templates', output_path)
    
    # Ensure directory exists
    ensure_directory(output_path)
    
    with open(output_path, 'w') as f:
        yaml.dump(templates[resource_type], f, default_flow_style=False)
    click.echo(f"Template generated at: {output_path}")

def terraform_plan(config_path: str):
    """Run terraform plan with the specified config"""
    # First validate the config
    validate_yaml(config_path)
    
    # Run terraform plan
    result = subprocess.run(['terraform', 'plan'], capture_output=True, text=True)
    click.echo(result.stdout)
    if result.returncode != 0:
        click.echo("Terraform plan failed!", err=True)
        sys.exit(1)

@click.group()
def cli():
    """Datadog Terraform CLI - Simplify Datadog resource deployment"""
    pass

@cli.command()
@click.argument('resource_type')
@click.argument('output_path')
def template(resource_type: str, output_path: str):
    """Generate a template YAML configuration"""
    generate_template(resource_type, output_path)

@cli.command()
@click.argument('config_path')
def validate(config_path: str):
    """Validate a YAML configuration file"""
    config = validate_yaml(config_path)
    click.echo("Configuration is valid!")

@cli.command()
@click.argument('config_path')
def plan(config_path: str):
    """Preview changes to be applied"""
    terraform_plan(config_path)

@cli.command()
@click.argument('config_path')
def apply(config_path: str):
    """Apply the configuration"""
    # First do a plan
    terraform_plan(config_path)
    
    if click.confirm('Do you want to apply these changes?'):
        result = subprocess.run(['terraform', 'apply', '-auto-approve'], capture_output=True, text=True)
        click.echo(result.stdout)
        if result.returncode != 0:
            click.echo("Terraform apply failed!", err=True)
            sys.exit(1)

if __name__ == '__main__':
    cli()
