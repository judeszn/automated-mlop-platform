"""Flask application for Model Registry service"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from datetime import datetime

from database import Database

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize database
db = Database()


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "model-registry",
        "timestamp": datetime.utcnow().isoformat()
    }), 200


@app.route('/api/experiments/track', methods=['POST'])
def track_experiment():
    """
    Track experiment data
    
    Request body:
    {
        "experiment_name": "my_training",
        "parameters": {"learning_rate": 0.01, "epochs": 100},
        "start_time": "2026-02-05T10:00:00",
        "status": "running"
    }
    """
    try:
        data = request.get_json()
        
        if not data or "experiment_name" not in data:
            return jsonify({
                "error": "experiment_name is required"
            }), 400
        
        # Save experiment to database
        experiment_id = db.save_experiment(data)
        
        logger.info(f"Tracked experiment: {experiment_id} - {data.get('experiment_name')}")
        
        return jsonify({
            "status": "success",
            "experiment_id": experiment_id,
            "message": f"Experiment {experiment_id} tracked successfully"
        }), 201
        
    except Exception as e:
        logger.error(f"Error tracking experiment: {e}")
        return jsonify({
            "error": str(e)
        }), 500


@app.route('/api/experiments/<experiment_id>', methods=['GET'])
def get_experiment(experiment_id):
    """Get experiment details by ID"""
    try:
        experiment = db.get_experiment(experiment_id)
        
        if not experiment:
            return jsonify({
                "error": "Experiment not found"
            }), 404
        
        return jsonify(experiment), 200
        
    except Exception as e:
        logger.error(f"Error retrieving experiment: {e}")
        return jsonify({
            "error": str(e)
        }), 500


@app.route('/api/experiments', methods=['GET'])
def list_experiments():
    """List all experiments"""
    try:
        limit = request.args.get('limit', 100, type=int)
        experiments = db.get_all_experiments(limit=limit)
        
        return jsonify({
            "experiments": experiments,
            "count": len(experiments)
        }), 200
        
    except Exception as e:
        logger.error(f"Error listing experiments: {e}")
        return jsonify({
            "error": str(e)
        }), 500


@app.route('/api/experiments/<experiment_id>/metrics', methods=['POST'])
def log_metric(experiment_id):
    """
    Log a metric for an experiment
    
    Request body:
    {
        "key": "accuracy",
        "value": 0.95,
        "step": 1
    }
    """
    try:
        data = request.get_json()
        
        if not data or "key" not in data or "value" not in data:
            return jsonify({
                "error": "key and value are required"
            }), 400
        
        db.log_metric(
            experiment_id,
            data["key"],
            float(data["value"]),
            data.get("step")
        )
        
        return jsonify({
            "status": "success",
            "message": f"Metric logged for experiment {experiment_id}"
        }), 201
        
    except Exception as e:
        logger.error(f"Error logging metric: {e}")
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == '__main__':
    logger.info("Starting Model Registry service...")
    app.run(host='0.0.0.0', port=5000, debug=True)
