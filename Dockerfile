# Example Dockerfile for a Python Flask application
# Use a slim base image for smaller size
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Cloud Run will inject the PORT environment variable.
# Your application should listen on 0.0.0.0 and the port specified by this variable.
# EXPOSE 8080 # This is optional, but good practice

# Command to run your application
# For Flask, you might use Gunicorn or another WSGI server
CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "app:app"]
