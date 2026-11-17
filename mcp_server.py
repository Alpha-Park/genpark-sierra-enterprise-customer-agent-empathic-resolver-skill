#!/usr/bin/env python3
import json
import sys
from client import SierraEnterpriseCustomerAgentEmpathicResolver

from typing import Any, Dict, List, Optional

try:
    from mcp.server.fastmcp import FastMCP
except ImportError as exc:
    raise SystemExit("MCP requires the mcp package. Run: python -m pip install -r requirements.txt") from exc

mcp = FastMCP('genpark-sierra-enterprise-customer-agent-empathic-resolver-skill')

@mcp.tool()
def resolve_customer_inquiry(customer_message: str = "", action_requested: str = "", order_context: Optional[Dict[str, Any]] = None) -> str:
    """Resolve a customer inquiry using the existing sentiment and policy checks."""
    return json.dumps(SierraEnterpriseCustomerAgentEmpathicResolver().resolve_customer_inquiry(customer_message, action_requested, order_context if order_context is not None else {}))

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        resolver = SierraEnterpriseCustomerAgentEmpathicResolver()
        msg = "This is unacceptable! The item arrived broken and I want an immediate refund!"
        order = {"order_id": "ORD-8821", "days_since_delivery": 5, "order_amount_usd": 89.0, "order_status": "DELIVERED"}
        res = resolver.resolve_customer_inquiry(msg, "refund_request", order)
        assert res["final_status"] == "RESOLVED_AUTONOMOUSLY"
        assert res["sentiment_audit"]["empathy_required"] is True
        print(f"[TEST PASS] Sierra Customer Agent Passed! Status: {res['final_status']}")
        sys.exit(0)

    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
