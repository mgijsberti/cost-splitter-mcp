#!/bin/sh

set -e

echo "===================="
echo "Running unit tests"
echo "===================="
uv run pytest test_main.py -v

echo "\n========================="
echo "Running integration test"
echo "========================="

# Free up port 8000 if in use
if lsof -i :8000 | grep LISTEN; then
  PID=$(lsof -ti :8000)
  echo "Port 8000 in use by PID $PID, killing..."
  kill -9 $PID
  sleep 1
fi

# Start the service in the background
uv run main.py &
SERVICE_PID=$!

# Wait for the service to be ready (up to 20 seconds)
for i in $(seq 1 20); do
  if curl -s http://127.0.0.1:8000/mcp/ > /dev/null; then
    break
  fi
  sleep 1
done

# Run the integration test
uv run python test_integration_stdio.py

# Kill the service gracefully, then force if needed
kill $SERVICE_PID
sleep 2
if kill -0 $SERVICE_PID 2>/dev/null; then
  echo "Service did not shut down, force killing..."
  kill -9 $SERVICE_PID
fi
wait $SERVICE_PID 2>/dev/null || true 