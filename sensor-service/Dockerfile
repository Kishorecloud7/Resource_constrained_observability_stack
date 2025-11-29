# -----------------------------
# Stage 1: Build Dependencies
# -----------------------------
FROM python:3.11-slim AS base

# Ensure no Python bytecode + faster container start
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# -----------------------------
# Stage 2: Final Runtime Image
# -----------------------------
FROM python:3.11-slim

WORKDIR /app

# Copy only necessary files
COPY --from=base /usr/local /usr/local
COPY sensor.py .
COPY configs/ configs/

EXPOSE 8000

# Start the service using Gunicorn (production-grade)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "sensor:app"]
