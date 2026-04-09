# Use the official Python slim image
FROM python:3.11-slim

# Allow statements and log messages to immediately appear in the logs
ENV PYTHONUNBUFFERED True

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Cloud Run injects the PORT environment variable. 
# Use Gunicorn as a production-grade WSGI server.
# Change 'main:app' to the actual entry point of your Flask/FastAPI app.
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
