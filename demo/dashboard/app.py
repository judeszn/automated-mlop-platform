"""
Mock Monitoring Dashboard - Beautiful visualization for demo
Shows real-time metrics, model performance, and deployment status
"""

from flask import Flask, render_template, jsonify
from flask_cors import CORS
import random
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    """Main dashboard view"""
    return render_template('dashboard.html')


@app.route('/api/metrics/realtime')
def realtime_metrics():
    """Mock real-time metrics for live demo"""
    return jsonify({
        "timestamp": datetime.utcnow().isoformat(),
            "models_deployed": 3,
        "active_experiments": 12,
        "predictions_today": 145234,
        "avg_latency_ms": 45,
        "success_rate": 99.98,
        "models": [
            {
                "name": "fraud-detector",
                "version": "1.2.3",
                "status": "healthy",
                "requests_per_min": 1240,
                "latency_p95": 43,
                "accuracy": 0.96
            },
            {
                "name": "recommendation-engine",
                "version": "2.0.1",
                "status": "healthy",
                "requests_per_min": 3450,
                "latency_p95": 28,
                "accuracy": 0.94
            },
            {
                "name": "sentiment-analyzer",
                "version": "1.0.5",
                "status": "healthy",
                "requests_per_min": 890,
                "latency_p95": 52,
                "accuracy": 0.91
            }
        ]
    })


@app.route('/api/experiments/recent')
def recent_experiments():
    """Mock recent experiments for demo"""
    experiments = []
    for i in range(10):
        created = datetime.utcnow() - timedelta(hours=i*2)
        experiments.append({
            "id": f"exp_{created.strftime('%Y%m%d_%H%M%S')}",
            "name": f"model_training_v{i+1}",
            "status": "completed",
            "accuracy": round(0.85 + random.random() * 0.1, 4),
            "duration": round(random.uniform(120, 600), 1),
            "created_at": created.isoformat()
        })
    return jsonify({"experiments": experiments})


if __name__ == '__main__':
    print("=" * 60)
    print("MLOps Monitoring Dashboard")
    print("=" * 60)
    print("Dashboard URL: http://localhost:3000")
    print("=" * 60)
    app.run(host='0.0.0.0', port=3000, debug=False)
