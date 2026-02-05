FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir flask flask-cors scikit-learn numpy

COPY . .

EXPOSE 8080

CMD ["python", "serve.py"]
