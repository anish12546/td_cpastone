from agents.profile_agent import analyze_profile
from agents.risk_agent import analyze_risk
from agents.decision_agent import make_decision
from agents.compliance_agent import log_compliance


def orchestrate(data):

    profile = analyze_profile(data)
    risk = analyze_risk(data)

    decision = make_decision(profile, risk)

    compliance = log_compliance(decision)

    return {
        "classification": decision["classification"],
        "risk_score": decision["risk_score"],
        "confidence": decision["confidence"],
        "explanation": decision["explanation"],
        "compliance": compliance
    }