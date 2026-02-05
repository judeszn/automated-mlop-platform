"""MLOps CLI - Command line interface for the MLOps platform"""

import click
import sys
import os
from datetime import datetime

# Add parent directory to path to import mlops_sdk
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


@click.group()
@click.version_option(version='0.1.0')
def cli():
    """MLOps Platform CLI - Manage ML models and deployments"""
    pass


@cli.command()
@click.option('--model-name', '-m', required=True, help='Name of the model to deploy')
@click.option('--version', '-v', default='latest', help='Model version to deploy')
@click.option('--environment', '-e', default='staging', 
              type=click.Choice(['dev', 'staging', 'production']),
              help='Target deployment environment')
@click.option('--replicas', '-r', default=2, type=int, help='Number of replicas')
@click.option('--cpu', default='500m', help='CPU request (e.g., 500m, 1)')
@click.option('--memory', default='1Gi', help='Memory request (e.g., 512Mi, 1Gi)')
def deploy(model_name, version, environment, replicas, cpu, memory):
    """
    Generate and display a deployment plan for a model
    
    Example:
        mlops deploy -m my_model -v 1.2.0 -e production
    """
    click.echo()
    click.secho("=" * 70, fg='cyan', bold=True)
    click.secho("  MLOps Deployment Plan", fg='cyan', bold=True)
    click.secho("=" * 70, fg='cyan', bold=True)
    click.echo()
    
    # Model Information
    click.secho(" Model Information", fg='yellow', bold=True)
    click.echo(f"   Name:        {model_name}")
    click.echo(f"   Version:     {version}")
    click.echo(f"   Environment: {environment}")
    click.echo()
    
    # Deployment Configuration
    click.secho("  Deployment Configuration", fg='yellow', bold=True)
    click.echo(f"   Replicas:    {replicas}")
    click.echo(f"   CPU:         {cpu}")
    click.echo(f"   Memory:      {memory}")
    click.echo()
    
    # Infrastructure Plan
    click.secho("  Infrastructure Plan", fg='yellow', bold=True)
    click.echo(f"   ✓ Create Kubernetes Deployment: {model_name}-{version}")
    click.echo(f"   ✓ Create Service: {model_name}-service")
    click.echo(f"   ✓ Create Ingress: {model_name}.{environment}.mlops.local")
    click.echo(f"   ✓ Configure Horizontal Pod Autoscaler (HPA)")
    click.echo()
    
    # Resource Allocation
    click.secho("  Resource Allocation", fg='yellow', bold=True)
    click.echo(f"   Pod Resources:")
    click.echo(f"     - CPU Request:    {cpu}")
    click.echo(f"     - Memory Request: {memory}")
    click.echo(f"     - CPU Limit:      {_calculate_limit(cpu)}")
    click.echo(f"     - Memory Limit:   {_calculate_limit(memory)}")
    click.echo()
    
    # Monitoring & Observability
    click.secho("  Monitoring & Observability", fg='yellow', bold=True)
    click.echo(f"   ✓ Enable Prometheus metrics endpoint")
    click.echo(f"   ✓ Configure Grafana dashboard")
    click.echo(f"   ✓ Set up log aggregation (ELK/Loki)")
    click.echo(f"   ✓ Create alerts for model performance degradation")
    click.echo()
    
    # Deployment Steps
    click.secho("  Deployment Steps", fg='yellow', bold=True)
    steps = [
        "1. Pull model artifacts from registry",
        "2. Build Docker container image",
        "3. Push image to container registry",
        "4. Apply Kubernetes manifests",
        "5. Wait for pods to be ready",
        "6. Run health checks",
        "7. Update DNS/routing",
        "8. Monitor initial traffic"
    ]
    for step in steps:
        click.echo(f"   {step}")
    click.echo()
    
    # Estimated Timeline
    click.secho("  Estimated Timeline", fg='yellow', bold=True)
    click.echo(f"   Build & Push:     ~3 minutes")
    click.echo(f"   Deploy & Scale:   ~2 minutes")
    click.echo(f"   Health Checks:    ~1 minute")
    click.echo(f"   Total Duration:   ~6 minutes")
    click.echo()
    
    # Rollback Plan
    click.secho("  Rollback Plan", fg='yellow', bold=True)
    click.echo(f"   Previous Version: {_get_previous_version(version)}")
    click.echo(f"   Rollback Command: mlops rollback -m {model_name} -e {environment}")
    click.echo()
    
    click.secho("=" * 70, fg='cyan', bold=True)
    click.echo()
    
    # Confirmation prompt
    if environment == 'production':
        click.secho("  WARNING: Deploying to PRODUCTION environment!", fg='red', bold=True)
        if not click.confirm('Do you want to proceed with this deployment?'):
            click.secho(" Deployment cancelled", fg='red')
            return
    
    click.secho(" Deployment plan generated successfully!", fg='green', bold=True)
    click.echo()
    click.secho(" Next steps:", fg='yellow')
    click.echo(f"   - Review the plan above")
    click.echo(f"   - Run: mlops deploy -m {model_name} --apply  (to actually deploy)")
    click.echo(f"   - Monitor: mlops status -m {model_name}")
    click.echo()


@cli.command()
@click.option('--model-name', '-m', help='Filter by model name')
def list(model_name):
    """List all deployed models"""
    click.secho("\n  Deployed Models\n", fg='cyan', bold=True)
    
    # Mock data
    models = [
        {"name": "fraud-detector", "version": "1.2.3", "env": "production", "status": "healthy"},
        {"name": "recommendation-engine", "version": "2.0.1", "env": "production", "status": "healthy"},
        {"name": "sentiment-analyzer", "version": "1.0.5", "env": "staging", "status": "degraded"},
    ]
    
    if model_name:
        models = [m for m in models if model_name.lower() in m["name"].lower()]
    
    for model in models:
        status_color = 'green' if model['status'] == 'healthy' else 'yellow'
        click.echo(f"  • {model['name']} (v{model['version']}) - {model['env']}")
        click.secho(f"    Status: {model['status']}", fg=status_color)
    
    click.echo()


@cli.command()
@click.option('--model-name', '-m', required=True, help='Name of the model')
def status(model_name):
    """Check deployment status of a model"""
    click.secho(f"\n  Status for {model_name}\n", fg='cyan', bold=True)
    
    click.echo("  Environment:  production")
    click.echo("  Version:      1.2.3")
    click.echo("  Replicas:     2/2 ready")
    click.secho("  Health:       ✓ Healthy", fg='green')
    click.echo("  Uptime:       5d 12h 34m")
    click.echo("\n  Metrics (last 1h):")
    click.echo("    Requests:   145,234")
    click.echo("    Latency:    45ms (p95)")
    click.echo("    Errors:     0.02%")
    click.echo()


def _calculate_limit(request_value):
    """Calculate resource limit (2x the request)"""
    if request_value.endswith('m'):
        return f"{int(request_value[:-1]) * 2}m"
    elif request_value.endswith('Gi'):
        return f"{int(request_value[:-2]) * 2}Gi"
    elif request_value.endswith('Mi'):
        return f"{int(request_value[:-2]) * 2}Mi"
    return request_value


def _get_previous_version(current_version):
    """Get previous version for rollback"""
    if current_version == 'latest':
        return '1.0.0'
    parts = current_version.split('.')
    if len(parts) == 3:
        try:
            patch = int(parts[2]) - 1
            if patch >= 0:
                return f"{parts[0]}.{parts[1]}.{patch}"
        except ValueError:
            pass
    return '1.0.0'


if __name__ == '__main__':
    cli()
