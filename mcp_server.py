#!/usr/bin/env python3
import json
import sys
from client import SierraEnterpriseCustomerAgentEmpathicResolver

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

    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            method = req.get("method")
            msg_id = req.get("id")
            if method == "initialize":
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"serverInfo": {"name": "genpark-sierra-agent", "version": "1.0.0"}}}))
            elif method == "tools/list":
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"tools": [{"name": "resolve_customer_inquiry", "description": "Sierra customer support agent with empathetic resolution and policy guardrails"}]}}))
            elif method == "tools/call":
                args = req.get("params", {}).get("arguments", {})
                resolver = SierraEnterpriseCustomerAgentEmpathicResolver()
                out = resolver.resolve_customer_inquiry(args.get("customer_message", ""), args.get("action_requested", ""), args.get("order_context", {}))
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"content": [{"type": "text", "text": json.dumps(out)}]}}))
            else:
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": "Method not found"}}))
            sys.stdout.flush()
        except Exception as e:
            print(json.dumps({"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}}))
            sys.stdout.flush()

if __name__ == "__main__":
    main()
