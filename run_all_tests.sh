#!/bin/sh

set -e

echo "===================="
echo "Running unit tests"
echo "===================="
uv run pytest test_main.py -v

echo "\n========================="
echo "Running integration test"
echo "========================="
uv run python test_integration_stdio.py 