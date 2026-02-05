#!/bin/bash

echo "╔════════════════════════════════════════════════════════════╗"
echo "║           MLOps Platform - Demo Setup                      ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop first."
    exit 1
fi

echo "✅ Docker is running"
echo ""

# Stop any existing containers
echo "🧹 Cleaning up existing containers..."
docker-compose down -v 2>/dev/null
lsof -ti:5000 2>/dev/null | xargs kill -9 2>/dev/null || true
lsof -ti:3000 2>/dev/null | xargs kill -9 2>/dev/null || true
lsof -ti:8080 2>/dev/null | xargs kill -9 2>/dev/null || true

echo ""
echo "🚀 Starting MLOps Platform..."
echo ""

# Start services
docker-compose up -d --build

echo ""
echo "⏳ Waiting for services to be ready (30 seconds)..."
sleep 30

echo ""
echo "✅ Platform is ready!"
echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                    Access Points                           ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "  📊 Dashboard:     http://localhost:3000"
echo "  🤖 Model API:     http://localhost:8080"
echo "  📦 Registry:      http://localhost:5000"
echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                    Quick Tests                             ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "  Test prediction:"
echo "  curl -X POST http://localhost:8080/predict \\"
echo "    -H 'Content-Type: application/json' \\"
echo "    -d '{\"features\": {\"amount\": 5000}}'"
echo ""
echo "  Deploy command:"
echo "  mlops deploy -m fraud-detector -v 1.2.3 -e production"
echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║  Opening dashboard in browser...                           ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Try to open browser
if command -v open &> /dev/null; then
    open http://localhost:3000
elif command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:3000
fi

echo ""
echo "✅ Demo is ready! Follow DEMO_SCRIPT.md for the presentation."
echo ""
