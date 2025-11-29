#!/bin/bash

# -----------------------------------------
# CPU Profiling Script for Sensor Service
# -----------------------------------------
# This script repeatedly calls the sensor API
# to trigger CPU spikes and observes resource usage.
#
# Usage:
#   chmod +x profile_cpu.sh
#   ./profile_cpu.sh
# -----------------------------------------

SENSOR_URL="http://localhost:8000/"
INTERVAL=1   # seconds between requests

echo "Starting CPU profiling against: $SENSOR_URL"
echo "Press CTRL+C to stop."
echo "-----------------------------------------"

# Start docker stats in background to observe CPU/Memory
echo "Starting docker stats (monitoring sensor-service container)..."
docker stats sensor-service --no-stream &
STATS_PID=$!

# Main loop hitting the API to stress the service
while true; do
    curl -s $SENSOR_URL > /dev/null
    echo "[Request Sent] $(date)"
    sleep $INTERVAL
done

# Cleanup on exit
trap "kill $STATS_PID 2>/dev/null" EXIT
