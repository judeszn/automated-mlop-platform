"""
Demo: MLOps CLI Usage

This script demonstrates the CLI commands available in the platform.
"""

import subprocess
import sys

def run_command(cmd, description):
    """Run a shell command and display output"""
    print("\n" + "="*70)
    print(f"📌 {description}")
    print("="*70)
    print(f"Command: {cmd}\n")
    
    result = subprocess.run(cmd, shell=True, capture_output=False, text=True)
    
    if result.returncode != 0:
        print(f"\n⚠️  Command exited with code {result.returncode}")
    
    return result.returncode == 0


if __name__ == "__main__":
    print("\n" + "="*70)
    print("MLOps CLI - Demo")
    print("="*70)
    print("\nThis demo shows the available CLI commands.")
    print("="*70 + "\n")
    
    # Install SDK first
    print("First, install the SDK:")
    print("  cd sdk && pip install -e .\n")
    
    input("Press Enter after installing to continue...")
    
    # Demo 1: Deploy command
    run_command(
        "mlops deploy -m fraud-detector -v 1.2.0 -e staging -r 3",
        "Generate deployment plan for a model"
    )
    
    input("\nPress Enter to continue...")
    
    # Demo 2: List models
    run_command(
        "mlops list",
        "List all deployed models"
    )
    
    input("\nPress Enter to continue...")
    
    # Demo 3: Check status
    run_command(
        "mlops status -m fraud-detector",
        "Check status of a specific model"
    )
    
    input("\nPress Enter to continue...")
    
    # Demo 4: Production deployment
    run_command(
        "mlops deploy -m recommendation-engine -v 2.1.0 -e production --cpu 1 --memory 2Gi",
        "Production deployment with resource specifications"
    )
    
    print("\n" + "="*70)
    print("✅ CLI Demo Complete!")
    print("="*70)
    print("\nAvailable commands:")
    print("  mlops deploy  - Generate deployment plan")
    print("  mlops list    - List deployed models")
    print("  mlops status  - Check model status")
    print("  mlops --help  - Show all options")
    print("="*70 + "\n")
