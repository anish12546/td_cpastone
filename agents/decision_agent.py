from communication.mcp_server import mcp_client
from services.claude_integration import explain_decision

def make_decision(profile, risk):

    mcp_client.send("decision_agent", {"profile": profile, "risk": risk})

    if (
        profile["income_stability"] == "High"
        and risk["credit_risk"] == "Low"
        and risk["anomaly"] is False
    ):
        classification = "Approved"
        confidence = 0.9

    elif risk["credit_risk"] == "High" or risk["anomaly"] is True:
        classification = "Rejected"
        confidence = 0.8

    else:
        classification = "Review"
        confidence = 0.6

    decision = {
        "classification": classification,
        "risk_score": risk["risk_score"],
        "confidence": confidence
    }

    explanation = explain_decision(profile, risk, decision)

    decision["explanation"] = explanation

    return decision