FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY sensor.py .

# Expose API + Metrics ports
EXPOSE 8000
EXPOSE 8001

# Start the sensor service
CMD ["python", "sensor.py"]
