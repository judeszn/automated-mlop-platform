"""
Demo: Basic ML Experiment Tracking

This example shows how to use the @track_experiment decorator
to automatically log your ML experiments.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from mlops_sdk import track_experiment, log_metric
import time
import random


@track_experiment("simple_model_training")
def train_simple_model(learning_rate=0.01, epochs=10, batch_size=32):
    """
    A simple mock training function that demonstrates experiment tracking
    """
    print(f"\n{'='*60}")
    print(f"Starting Training with:")
    print(f"  Learning Rate: {learning_rate}")
    print(f"  Epochs: {epochs}")
    print(f"  Batch Size: {batch_size}")
    print(f"{'='*60}\n")
    
    # Simulate training
    for epoch in range(epochs):
        # Simulate training time
        time.sleep(0.2)
        
        # Mock metrics that improve over time
        accuracy = 0.5 + (epoch / epochs) * 0.45 + random.uniform(-0.02, 0.02)
        loss = 1.0 - (epoch / epochs) * 0.7 + random.uniform(-0.05, 0.05)
        
        print(f"Epoch {epoch + 1}/{epochs} - Accuracy: {accuracy:.4f}, Loss: {loss:.4f}")
        
        # Log metrics (these would be sent to backend)
        log_metric("accuracy", accuracy, step=epoch)
        log_metric("loss", loss, step=epoch)
    
    final_accuracy = 0.95
    print(f"\n{'='*60}")
    print(f"Training Complete!")
    print(f"Final Accuracy: {final_accuracy:.4f}")
    print(f"{'='*60}\n")
    
    return final_accuracy


@track_experiment("hyperparameter_tuning")
def run_hyperparameter_search(n_trials=3):
    """
    Simulate hyperparameter tuning with multiple experiments
    """
    print(f"\n{'='*60}")
    print(f"Running Hyperparameter Search ({n_trials} trials)")
    print(f"{'='*60}\n")
    
    best_accuracy = 0
    best_params = {}
    
    for trial in range(n_trials):
        lr = random.choice([0.001, 0.01, 0.1])
        batch_size = random.choice([16, 32, 64])
        
        print(f"\nTrial {trial + 1}/{n_trials}: lr={lr}, batch_size={batch_size}")
        
        # This will also be tracked automatically
        accuracy = train_simple_model(
            learning_rate=lr,
            epochs=5,
            batch_size=batch_size
        )
        
        if accuracy > best_accuracy:
            best_accuracy = accuracy
            best_params = {"learning_rate": lr, "batch_size": batch_size}
    
    print(f"\n{'='*60}")
    print(f"Best Parameters: {best_params}")
    print(f"Best Accuracy: {best_accuracy:.4f}")
    print(f"{'='*60}\n")
    
    return best_params


if __name__ == "__main__":
    print("\n" + "="*60)
    print("MLOps SDK - Experiment Tracking Demo")
    print("="*60)
    print("\nThis demo shows automatic experiment tracking.")
    print("Make sure the backend is running: python backend/model-registry/run.py")
    print("="*60 + "\n")
    
    # Example 1: Single training run
    print("\n📊 Example 1: Single Training Run")
    result = train_simple_model(learning_rate=0.001, epochs=10, batch_size=32)
    
    print("\n" + "="*60)
    input("Press Enter to continue to hyperparameter search...")
    
    # Example 2: Hyperparameter tuning
    print("\n📊 Example 2: Hyperparameter Tuning")
    best_params = run_hyperparameter_search(n_trials=3)
    
    print("\n✅ Demo complete! Check the backend logs to see tracked experiments.")
