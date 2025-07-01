#!/bin/sh

curl -X POST http://127.0.0.1:8000/mcp/infer \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "x-session-id: test-session" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "infer",
    "params": {
      "tool": "equalize_costs",
      "args": {
        "people": [
          {"name": "Alice", "paid": 100},
          {"name": "Bob", "paid": 60},
          {"name": "Charlie", "paid": 40},
          {"name": "David", "paid": 20}
        ]
      }
    }
  }'
echo 