# MLOps SDK

Python SDK for the Automated MLOps Platform.

## Installation

```bash
pip install -e .
```

## Quick Start

### Track Experiments

```python
from mlops_sdk import track_experiment

@track_experiment("my_model_training")
def train_model(learning_rate=0.01, epochs=100):
    # Your training code here
    accuracy = 0.95
    return accuracy

# Run your training
result = train_model(learning_rate=0.001, epochs=50)
```

### Manual Logging

```python
from mlops_sdk import set_experiment, log_param, log_metric

set_experiment("custom_experiment")
log_param("model_type", "random_forest")
log_param("n_estimators", 100)

# During training
log_metric("accuracy", 0.95, step=1)
log_metric("loss", 0.05, step=1)
```

## Features

- **@track_experiment**: Decorator for automatic experiment tracking
- **log_param**: Log hyperparameters
- **log_metric**: Log training metrics
- **Offline mode**: Works even when backend is not available
