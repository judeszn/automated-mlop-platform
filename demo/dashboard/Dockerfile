FROM python:3.11-slim

WORKDIR /app

# Install minimal dependencies
RUN pip install --no-cache-dir flask flask-cors

# Copy dashboard code
COPY . .

EXPOSE 3000

CMD ["python", "app.py"]
