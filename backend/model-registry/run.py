"""Entry point to run the Model Registry service"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, logger

if __name__ == '__main__':
    logger.info("=" * 60)
    logger.info("MLOps Model Registry Service")
    logger.info("=" * 60)
    logger.info("API Endpoints:")
    logger.info("  GET  /health - Health check")
    logger.info("  POST /api/experiments/track - Track experiment")
    logger.info("  GET  /api/experiments - List all experiments")
    logger.info("  GET  /api/experiments/<id> - Get experiment details")
    logger.info("  POST /api/experiments/<id>/metrics - Log metric")
    logger.info("=" * 60)
    logger.info("Starting server on http://localhost:5000")
    logger.info("=" * 60)
    
    app.run(host='0.0.0.0', port=5000, debug=True)
