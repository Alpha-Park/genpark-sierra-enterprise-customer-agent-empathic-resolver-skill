from client import SierraEnterpriseCustomerAgentEmpathicResolver

def main():
    resolver = SierraEnterpriseCustomerAgentEmpathicResolver()
    msg = "I am furious that my order was delayed. Can I change my delivery address?"
    order = {"order_id": "ORD-5541", "order_status": "SHIPPED", "days_since_delivery": 0, "order_amount_usd": 120.0}
    res = resolver.resolve_customer_inquiry(msg, "address_change", order)
    print("--- Sierra Enterprise Customer Agent Output ---")
    print(f"Sentiment: {res['sentiment_audit']['sentiment']} (Triggers: {res['sentiment_audit']['detected_triggers']})")
    print(f"Policy Check: {res['policy_check']['reason']}")
    print(f"Final Status: {res['final_status']}")
    print(f"Response:\n{res['agent_response']}")

if __name__ == "__main__":
    main()
