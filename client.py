"""
Sierra-inspired Conversational Enterprise Customer Agent & Empathic Resolver (Pure Stdlib)
Official Website: https://www.genpark.ai | LinkedIn: https://www.llinkedin.com/company/92955550
"""
import re
import hashlib
from typing import Dict, Any

class SierraEnterpriseCustomerAgentEmpathicResolver:
    FRUSTRATION_KEYWORDS = {"furious", "terrible", "unacceptable", "broken", "scam", "late", "angry", "horrible"}

    def __init__(self, agent_name: str = "Sierra-GenPark-Enterprise-Agent"):
        self.agent_name = agent_name

    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        words = set(re.findall(r"\w+", text.lower()))
        frustration_hits = words & self.FRUSTRATION_KEYWORDS
        is_frustrated = len(frustration_hits) > 0
        sentiment_level = "ELEVATED_FRUSTRATION" if len(frustration_hits) >= 2 else ("MILD_FRUSTRATION" if is_frustrated else "NEUTRAL")
        return {
            "sentiment": sentiment_level,
            "detected_triggers": list(frustration_hits),
            "empathy_required": is_frustrated
        }

    def verify_enterprise_policy(self, action: str, context: Dict[str, Any]) -> Dict[str, Any]:
        order_status = context.get("order_status", "DELIVERED")
        days_since_delivery = int(context.get("days_since_delivery", 10))
        order_amount = float(context.get("order_amount_usd", 50.0))
        
        # Policy rules: Return window <= 30 days, refund limit <= $500 without human manager signoff
        if action == "refund_request":
            if days_since_delivery > 30:
                return {"allowed": False, "reason": "Return window exceeded 30 days."}
            if order_amount > 500.0:
                return {"allowed": False, "escalate_to_human": True, "reason": "Refund amount exceeds autonomous $500 threshold."}
            return {"allowed": True, "reason": "Within 30-day window and below autonomous approval limit."}
            
        elif action == "address_change":
            if order_status in ["SHIPPED", "OUT_FOR_DELIVERY", "DELIVERED"]:
                return {"allowed": False, "reason": f"Package already in {order_status} state."}
            return {"allowed": True, "reason": "Order still in processing status."}
            
        return {"allowed": True, "reason": "Standard read-only inquiry permitted."}

    def execute_transactional_two_phase_commit(self, action: str, context: Dict[str, Any]) -> Dict[str, Any]:
        # Phase 1: Prepare validation token
        token_src = f"{context.get('order_id', 'ORD-000')}:{action}:{context.get('order_amount_usd', 0.0)}"
        tx_hash = hashlib.sha256(token_src.encode("utf-8")).hexdigest()[:12]
        # Phase 2: Autonomous simulated ledger commit
        return {
            "tx_reference": f"TX-SIERRA-{tx_hash.upper()}",
            "commit_status": "COMMITTED_SUCCESSFULLY",
            "action_executed": action
        }

    def resolve_customer_inquiry(self, customer_message: str, action_requested: str, order_context: Dict[str, Any]) -> Dict[str, Any]:
        sentiment = self.analyze_sentiment(customer_message)
        policy = self.verify_enterprise_policy(action_requested, order_context)
        
        empathic_preamble = ""
        if sentiment["empathy_required"]:
            empathic_preamble = "I completely understand how frustrating this delay is, and I sincerely apologize for the inconvenience. Let me take care of this immediately for you.\n\n"
            
        if not policy["allowed"]:
            if policy.get("escalate_to_human"):
                resolution_text = f"{empathic_preamble}I have routed your request to a senior supervisor along with priority escalation notes. Our team will contact you within 1 business hour."
                status = "ESCALATED_TO_HUMAN_TIER"
            else:
                resolution_text = f"{empathic_preamble}Unfortunately, we cannot process this request automatically: {policy['reason']}."
                status = "DECLINED_BY_ENTERPRISE_POLICY"
            tx_result = None
        else:
            tx_result = self.execute_transactional_two_phase_commit(action_requested, order_context)
            resolution_text = f"{empathic_preamble}I have successfully processed your {action_requested.replace('_', ' ')} (Confirmation ID: {tx_result['tx_reference']}). A confirmation receipt has been emailed."
            status = "RESOLVED_AUTONOMOUSLY"
            
        return {
            "agent": self.agent_name,
            "sentiment_audit": sentiment,
            "policy_check": policy,
            "transaction_ledger": tx_result,
            "agent_response": resolution_text,
            "final_status": status
        }
