#!/bin/bash

# -----------------------------------------
# Lightweight Load Test Script
# -----------------------------------------
# Sends multiple parallel requests to the sensor
# service to simulate heavy load and measure stability.
#
# Usage:
#   chmod +x load_test.sh
#   ./load_test.sh
# -----------------------------------------

TARGET_URL="http://localhost:8000/"
CONCURRENCY=20       # number of parallel workers
REQUESTS=200         # total number of requests

echo "Running load test..."
echo "Target:      $TARGET_URL"
echo "Requests:    $REQUESTS"
echo "Concurrency: $CONCURRENCY"
echo "-----------------------------------------"

# Function executed by each worker
send_request() {
    curl -s -o /dev/null -w "%{http_code}\n" "$TARGET_URL"
}

export -f send_request

# Run parallel requests
seq $REQUESTS | xargs -n1 -P$CONCURRENCY bash -c 'send_request'

echo "-----------------------------------------"
echo "Load test completed."
echo "Check metrics at: http://localhost:8000/metrics"
echo "Check VictoriaMetrics UI: http://localhost:8428/graph"
