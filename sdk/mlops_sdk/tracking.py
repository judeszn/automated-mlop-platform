"""Experiment tracking decorators and functions"""

import functools
import time
import inspect
from typing import Any, Callable, Dict, Optional
import logging
from datetime import datetime

from .client import MLOpsClient

logger = logging.getLogger(__name__)

# Global state
_active_experiment = None
_client = MLOpsClient()


def set_experiment(experiment_name: str):
    """Set the active experiment name"""
    global _active_experiment
    _active_experiment = experiment_name
    logger.info(f"Active experiment set to: {experiment_name}")


def log_param(key: str, value: Any):
    """Log a parameter for the current experiment"""
    if _active_experiment is None:
        logger.warning("No active experiment. Call set_experiment() first.")
        return
    logger.info(f"Logged param: {key}={value}")


def log_metric(key: str, value: float, step: Optional[int] = None):
    """Log a metric for the current experiment"""
    if _active_experiment is None:
        logger.warning("No active experiment. Call set_experiment() first.")
        return
    logger.info(f"Logged metric: {key}={value}" + (f" (step {step})" if step else ""))


def track_experiment(experiment_name: Optional[str] = None):
    """
    Decorator to automatically track ML experiments
    
    Usage:
        @track_experiment("my_model_training")
        def train_model(learning_rate=0.01, epochs=100):
            # Your training code
            accuracy = 0.95
            return accuracy
    
    Args:
        experiment_name: Optional name for the experiment. If not provided, uses function name.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Determine experiment name
            exp_name = experiment_name or func.__name__
            set_experiment(exp_name)
            
            # Extract function parameters
            sig = inspect.signature(func)
            bound_args = sig.bind_partial(*args, **kwargs)
            bound_args.apply_defaults()
            params = dict(bound_args.arguments)
            
            # Start tracking
            start_time = time.time()
            start_timestamp = datetime.utcnow().isoformat()
            
            logger.info(f"Starting experiment: {exp_name}")
            logger.info(f"Parameters: {params}")
            
            # Prepare experiment data
            experiment_data = {
                "experiment_name": exp_name,
                "parameters": params,
                "start_time": start_timestamp,
                "status": "running",
                "function_name": func.__name__,
                "module": func.__module__
            }
            
            # Track experiment start
            response = _client.track_experiment(experiment_data)
            experiment_id = response.get("experiment_id", "unknown")
            
            try:
                # Execute the actual function
                result = func(*args, **kwargs)
                
                # Calculate execution time
                end_time = time.time()
                duration = end_time - start_time
                end_timestamp = datetime.utcnow().isoformat()
                
                # Update experiment with results
                final_data = {
                    "experiment_id": experiment_id,
                    "experiment_name": exp_name,
                    "parameters": params,
                    "start_time": start_timestamp,
                    "end_time": end_timestamp,
                    "duration": duration,
                    "status": "completed",
                    "result": str(result) if result is not None else None
                }
                
                _client.track_experiment(final_data)
                
                logger.info(f"Experiment completed: {exp_name} (duration: {duration:.2f}s)")
                logger.info(f"Result: {result}")
                
                return result
                
            except Exception as e:
                # Track failure
                end_time = time.time()
                duration = end_time - start_time
                end_timestamp = datetime.utcnow().isoformat()
                
                error_data = {
                    "experiment_id": experiment_id,
                    "experiment_name": exp_name,
                    "parameters": params,
                    "start_time": start_timestamp,
                    "end_time": end_timestamp,
                    "duration": duration,
                    "status": "failed",
                    "error": str(e)
                }
                
                _client.track_experiment(error_data)
                logger.error(f"Experiment failed: {exp_name} - {e}")
                raise
        
        return wrapper
    return decorator
