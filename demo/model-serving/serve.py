"""
Mock Model Serving Endpoint - For demo purposes
Shows a working prediction API that clients will see
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import time
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Mock model
class MockModel:
    def predict(self, features):
        """Simulate prediction with realistic latency"""
        time.sleep(random.uniform(0.02, 0.05))  # 20-50ms latency
        
        # Return mock prediction
        if "fraud" in str(features).lower():
            return {"prediction": "fraudulent", "confidence": 0.94, "risk_score": 0.88}
        return {"prediction": "legitimate", "confidence": 0.92, "risk_score": 0.12}

model = MockModel()


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "model": "fraud-detector",
        "version": "1.2.3",
        "uptime": "5d 12h 34m"
    }), 200


@app.route('/predict', methods=['POST'])
def predict():
    """Main prediction endpoint"""
    start_time = time.time()
    
    try:
        data = request.get_json()
        
        if not data or 'features' not in data:
            return jsonify({"error": "Missing 'features' in request"}), 400
        
        # Make prediction
        result = model.predict(data['features'])
        
        latency = (time.time() - start_time) * 1000  # Convert to ms
        
        return jsonify({
            "prediction": result["prediction"],
            "confidence": result["confidence"],
            "risk_score": result["risk_score"],
            "model_version": "1.2.3",
            "latency_ms": round(latency, 2),
            "timestamp": datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/batch_predict', methods=['POST'])
def batch_predict():
    """Batch prediction endpoint"""
    data = request.get_json()
    
    if not data or 'batch' not in data:
        return jsonify({"error": "Missing 'batch' in request"}), 400
    
    predictions = []
    for item in data['batch']:
        result = model.predict(item.get('features', {}))
        predictions.append(result)
    
    return jsonify({
        "predictions": predictions,
        "count": len(predictions),
        "model_version": "1.2.3"
    }), 200


@app.route('/metrics', methods=['GET'])
def metrics():
    """Prometheus-style metrics endpoint"""
    metrics_text = f"""# HELP model_predictions_total Total number of predictions
# TYPE model_predictions_total counter
model_predictions_total{{model="fraud-detector",version="1.2.3"}} 145234

# HELP model_latency_seconds Prediction latency in seconds
# TYPE model_latency_seconds histogram
model_latency_seconds_bucket{{le="0.05"}} 142000
model_latency_seconds_bucket{{le="0.1"}} 145000
model_latency_seconds_bucket{{le="+Inf"}} 145234

# HELP model_accuracy Current model accuracy
# TYPE model_accuracy gauge
model_accuracy{{model="fraud-detector"}} 0.96
"""
    return metrics_text, 200, {'Content-Type': 'text/plain'}


if __name__ == '__main__':
    print("=" * 60)
    print("Model Serving API - fraud-detector v1.2.3")
    print("=" * 60)
    print("Prediction endpoint: http://localhost:8080/predict")
    print("Health check:        http://localhost:8080/health")
    print("=" * 60)
    app.run(host='0.0.0.0', port=8080, debug=False)
