import datetime


class MCPClient:

    def __init__(self):
        self.tools = {
            "profile_agent": self.profile_tool,
            "risk_agent": self.risk_tool,
            "decision_agent": self.decision_tool,
            "compliance_agent": self.compliance_tool,
            "credit_score_service": self.credit_score_tool,
            "employment_verification_service": self.employment_verification_tool
        }

    def send(self, agent_name, payload):
        print(f"[MCP] Sending request to: {agent_name}")

        if agent_name not in self.tools:
            return {
                "agent": agent_name,
                "status": "failed",
                "error": "Tool not registered"
            }

        response = self.tools[agent_name](payload)

        print(f"[MCP] Response from {agent_name}: {response}")

        return response

    def profile_tool(self, data):
        return {
            "tool_name": "profile_analysis_tool",
            "status": "executed",
            "timestamp": str(datetime.datetime.now()),
            "input_received": data
        }

    def risk_tool(self, data):
        return {
            "tool_name": "financial_risk_tool",
            "status": "executed",
            "timestamp": str(datetime.datetime.now()),
            "input_received": data
        }

    def decision_tool(self, data):
        return {
            "tool_name": "loan_decision_tool",
            "status": "executed",
            "timestamp": str(datetime.datetime.now()),
            "input_received": data
        }

    def compliance_tool(self, data):
        return {
            "tool_name": "compliance_audit_tool",
            "status": "executed",
            "timestamp": str(datetime.datetime.now()),
            "input_received": data
        }

    def credit_score_tool(self, data):
        return {
            "tool_name": "credit_score_service_tool",
            "status": "executed",
            "credit_score_checked": data.get("credit_score")
        }

    def employment_verification_tool(self, data):
        return {
            "tool_name": "employment_verification_tool",
            "status": "executed",
            "employment_type_checked": data.get("employment")
        }


mcp_client = MCPClient()