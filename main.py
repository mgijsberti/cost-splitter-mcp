"""Main module for the cost-splitter MCP service."""
import os
from typing import List
from fastmcp import FastMCP
from pydantic import BaseModel, Field

mcp = FastMCP()

# Cost-splitting logic
class Person(BaseModel):
    """Represents a person and the amount they paid."""
    name: str
    paid: float

class Transaction(BaseModel):
    """Represents a transaction from one person to another."""
    from_person: str = Field(alias="from")
    to: str
    amount: float

def split_costs(people: List[Person]) -> List[Transaction]:
    """Splits costs among people and returns the required transactions."""
    n = len(people)
    if n == 0:
        return []

    total = sum(p.paid for p in people)
    avg = total / n

    creditors = []
    debtors = []

    for p in people:
        diff = round(p.paid - avg, 2)
        if abs(diff) < 0.01:
            continue
        if diff > 0:
            creditors.append({"name": p.name, "amount": diff})
        else:
            debtors.append({"name": p.name, "amount": -diff})

    # Sort by amount (largest first) to ensure proper balancing
    creditors.sort(key=lambda x: x["amount"], reverse=True)
    debtors.sort(key=lambda x: x["amount"], reverse=True)

    transactions = []
    i = j = 0

    while i < len(debtors) and j < len(creditors):
        d = debtors[i]
        c = creditors[j]
        amount = round(min(d["amount"], c["amount"]), 2)

        transactions.append(Transaction(
            **{"from": d["name"], "to": c["name"], "amount": amount}
        ))

        d["amount"] -= amount
        c["amount"] -= amount

        if d["amount"] < 0.01:
            i += 1
        if c["amount"] < 0.01:
            j += 1

    return transactions

# Register the MCP tool
@mcp.tool()
def equalize_costs(people: List[Person]) -> List[Transaction]:
    """MCP tool to equalize costs among people."""
    return split_costs(people)

if __name__ == "__main__":
    if os.environ.get("TEST_MODE", "false").lower() == "true":
        print("[cost-splitter] Starting MCP server in HTTP (test) mode on 0.0.0.0:8000...")
        mcp.run(transport="http", host="0.0.0.0", port=8000)
    else:
        print("[cost-splitter] Starting MCP server in STDIO (Claude Desktop) mode...")
        mcp.run()
