# 🚀 Quick Start Guide

## One-Command Demo Launch

```bash
# Start everything
docker-compose up -d

# Wait 30 seconds for services to be ready
sleep 30

# Open dashboard
open http://localhost:3000
```

That's it. Everything is running.

## What's Running?

- **Dashboard:** http://localhost:3000 - Beautiful live metrics
- **Model API:** http://localhost:8080 - Live prediction endpoint
- **Registry:** http://localhost:5000 - Experiment tracking backend

## Run the Demo

1. **Install SDK:**
   ```bash
   cd sdk && pip install -e .
   ```

2. **Run demo notebook:**
   ```bash
   jupyter notebook demo/demo.ipynb
   ```

3. **Test prediction:**
   ```bash
   curl -X POST http://localhost:8080/predict \
     -H "Content-Type: application/json" \
     -d '{"features": {"amount": 5000}}'
   ```

4. **Deploy command:**
   ```bash
   mlops deploy -m fraud-detector -v 1.2.3 -e production
   ```

## Stop Everything

```bash
docker-compose down
```

## Troubleshooting

If port 5000 is busy:
```bash
lsof -ti:5000 | xargs kill -9
```

If containers won't start:
```bash
docker-compose down -v
docker-compose up --build
```
