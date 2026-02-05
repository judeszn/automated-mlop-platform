"""HTTP Client for communicating with MLOps backend"""

import os
import requests
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class MLOpsClient:
    """Client for interacting with MLOps backend API"""
    
    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or os.getenv("MLOPS_BACKEND_URL", "http://localhost:5000")
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
    
    def track_experiment(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send experiment tracking data to backend
        
        Args:
            data: Dictionary containing experiment data (name, params, metrics, etc.)
        
        Returns:
            Response from backend with experiment_id
        """
        try:
            response = self.session.post(
                f"{self.base_url}/api/experiments/track",
                json=data,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError:
            logger.warning(f"Could not connect to MLOps backend at {self.base_url}. Running in offline mode.")
            return {"experiment_id": "offline", "status": "offline"}
        except requests.exceptions.RequestException as e:
            logger.error(f"Error tracking experiment: {e}")
            return {"error": str(e)}
    
    def log_metric(self, experiment_id: str, key: str, value: float, step: Optional[int] = None):
        """Log a metric for an experiment"""
        try:
            response = self.session.post(
                f"{self.base_url}/api/experiments/{experiment_id}/metrics",
                json={"key": key, "value": value, "step": step},
                timeout=5
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error logging metric: {e}")
            return {"error": str(e)}
    
    def get_experiment(self, experiment_id: str) -> Dict[str, Any]:
        """Retrieve experiment details"""
        try:
            response = self.session.get(
                f"{self.base_url}/api/experiments/{experiment_id}",
                timeout=5
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting experiment: {e}")
            return {"error": str(e)}
