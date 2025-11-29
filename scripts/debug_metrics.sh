#!/bin/bash

# -----------------------------------------
# Metrics Debugging Script
# -----------------------------------------
# Fetches and displays Prometheus metrics from the
# sensor service, highlighting custom metrics.
#
# Usage:
#   chmod +x debug_metrics.sh
#   ./debug_metrics.sh
# -----------------------------------------

METRICS_URL="http://localhost:8000/metrics"

echo "Fetching metrics from: $METRICS_URL"
echo "-----------------------------------------"
echo ""

# Fetch complete metrics output
curl -s $METRICS_URL

echo ""
echo "-----------------------------------------"
echo "Custom Metrics (Filtered)"
echo "-----------------------------------------"

curl -s $METRICS_URL | grep -E "sensor_requests_total|sensor_failed_total|sensor_queue_depth|sensor_cpu_spike_seconds"

echo "-----------------------------------------"
echo "Done."
