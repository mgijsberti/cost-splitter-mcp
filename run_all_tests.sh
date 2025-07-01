#!/bin/sh

set -e

echo "===================="
echo "Running unit tests"
echo "===================="
uv run pytest test_main.py -v

echo "\n========================="
echo "Running integration test"
echo "========================="

# Start the service in the background
uv run main.py &
SERVICE_PID=$!

# Wait for the service to be ready
sleep 2

# Run the integration test
uv run python test_integration_stdio.py

# Kill the service
kill $SERVICE_PID 