"""Integration test for the cost-splitter MCP service using the FastMCP Python client library."""
# pylint: disable=line-too-long, missing-final-newline, too-many-locals
import json
import asyncio
from fastmcp import Client

# This script assumes the FastMCP server is running on localhost:8000 with HTTP transport

def run_fastmcp_client():
    """Runs the integration test for the cost-splitter MCP service."""
    asyncio.run(test_fastmcp_client())

async def test_fastmcp_client():
    """Test the equalize_costs tool using the FastMCP Python client."""
    client = Client("http://localhost:8000/mcp/")
    people = [
        {"name": "Alice", "paid": 100},
        {"name": "Bob", "paid": 60},
        {"name": "Charlie", "paid": 40},
        {"name": "David", "paid": 20}
    ]
    try:
        async with client:
            result = await client.call_tool("equalize_costs", {"people": people})
            print("Response:", result)
            assert result is not None, "Result should not be None"
            assert isinstance(result, list), "Result should be a list of transactions"
            assert len(result) > 0, "Should have at least one transaction"
            # Extract transaction data
            transactions = []
            for content in result:
                if hasattr(content, 'text') and hasattr(content, 'type') and content.type == 'text':
                    parsed_data = json.loads(content.text)
                    transactions.extend(parsed_data if isinstance(parsed_data, list) else [parsed_data])
                else:
                    transactions.append(content)
            if transactions:
                first_tx = transactions[0]
                print("Debug - First transaction structure:", first_tx)
                if isinstance(first_tx, dict):
                    print("Debug - Available keys:", list(first_tx.keys()))
                else:
                    print("Debug - Transaction type:", type(first_tx))
            # Validate transactions
            avg_paid = sum(p["paid"] for p in people) / len(people)
            net_received = {p["name"]: 0.0 for p in people}
            for tx in transactions:
                assert "from" in tx or "from_person" in tx, (
                    "Transaction should have 'from' field")
                assert "to" in tx, "Transaction should have 'to' field"
                assert "amount" in tx, "Transaction should have 'amount' field"
                assert isinstance(tx["amount"], (int, float)), (
                    "Amount should be numeric")
                assert tx["amount"] > 0, "Amount should be positive"
                from_person = tx.get("from") or tx.get("from_person")
                net_received[from_person] -= tx["amount"]
                net_received[tx["to"]] += tx["amount"]
            for name, received in net_received.items():
                original_paid = next(p["paid"] for p in people if p["name"] == name)
                net_payment = original_paid - received
                assert abs(net_payment - avg_paid) < 0.01, (
                    f"{name} should end up with average amount {avg_paid}, "
                    f"got {net_payment}")
            print("✅ All assertions passed! Integration test successful.")
    except Exception as e:
        print(f"❌ Error calling tool: {e}")
        raise

if __name__ == "__main__":
    run_fastmcp_client() 