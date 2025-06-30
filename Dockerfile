# syntax=docker/dockerfile:1

# Base image
FROM python:3.12-slim

# Set work directory
WORKDIR /app

# Install psycopg2 dependencies
RUN apt-get update && apt-get install -y gcc libpq-dev

# Copy requirements first (for caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire app
COPY . .

# Expose Flask's default port
EXPOSE 5000

# Environment variables for Flask
ENV FLASK_APP=run.py
ENV FLASK_ENV=development

# Run the app
CMD ["flask", "run", "--host=0.0.0.0"]
